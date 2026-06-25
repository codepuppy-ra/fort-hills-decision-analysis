"""Build monthly and annual WTI/WCS/AECO price panels."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INTERIM = ROOT / 'data' / 'interim'
CLEAN = ROOT / 'data' / 'cleaned'
CLEAN.mkdir(parents=True, exist_ok=True)


def monthly_average(df: pd.DataFrame, date_col: str, value_col: str) -> pd.DataFrame:
    temp = df.copy()
    temp[date_col] = pd.to_datetime(temp[date_col])
    temp['month'] = temp[date_col].dt.to_period('M').dt.to_timestamp()
    return temp.groupby('month', as_index=False)[value_col].mean()

wti = pd.read_csv(INTERIM / 'wti_daily.csv', parse_dates=['date'])
wcs = pd.read_csv(INTERIM / 'wcs_monthly.csv', parse_dates=['date'])
aeco = pd.read_csv(INTERIM / 'aeco_daily.csv', parse_dates=['date'])

wti_m = monthly_average(wti, 'date', 'wti_usd_bbl')
wcs_m = wcs.copy()
wcs_m['month'] = wcs_m['date'].dt.to_period('M').dt.to_timestamp()
wcs_m = wcs_m[['month', 'wcs_usd_bbl']]
aeco_m = monthly_average(aeco, 'date', 'aeco_cad_gj')

panel = wti_m.merge(wcs_m, on='month', how='outer').merge(aeco_m, on='month', how='outer')
panel = panel.sort_values('month')
panel['wti_wcs_diff_usd_bbl'] = panel['wti_usd_bbl'] - panel['wcs_usd_bbl']
panel['year'] = panel['month'].dt.year
panel.to_csv(CLEAN / 'monthly_price_panel.csv', index=False)

annual = panel.groupby('year', as_index=False).agg(
    wti_usd_bbl=('wti_usd_bbl', 'mean'),
    wcs_usd_bbl=('wcs_usd_bbl', 'mean'),
    wti_wcs_diff_usd_bbl=('wti_wcs_diff_usd_bbl', 'mean'),
    aeco_cad_gj=('aeco_cad_gj', 'mean'),
)
annual.to_csv(CLEAN / 'annual_price_panel.csv', index=False)

# Recent historical quantiles for scenario construction, using 2015+ to match modern oil sands context.
recent = panel[(panel['month'] >= '2015-01-01') & panel['wti_usd_bbl'].notna() & panel['wcs_usd_bbl'].notna()].copy()
qs = recent[['wti_usd_bbl', 'wti_wcs_diff_usd_bbl', 'wcs_usd_bbl']].quantile([0.1, 0.25, 0.5, 0.75, 0.9]).reset_index()
qs = qs.rename(columns={'index': 'quantile'})
qs.to_csv(CLEAN / 'recent_price_quantiles_2015_onward.csv', index=False)

print('Built cleaned price panels.')
print(f'Monthly panel: {panel.month.min().date()} to {panel.month.max().date()}, rows={len(panel):,}')
