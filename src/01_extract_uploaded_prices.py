"""Extract commodity-price data from the uploaded files.

The uploaded files are misnamed in places. This script standardizes them into:
- data/interim/wti_daily.csv
- data/interim/wcs_monthly.csv
- data/interim/aeco_daily.csv
- data/interim/factset_aeco_daily.csv
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
INTERIM = ROOT / 'data' / 'interim'
INTERIM.mkdir(parents=True, exist_ok=True)


def clean_date_price(df: pd.DataFrame, date_col: str, price_col: str, out_cols: tuple[str, str]) -> pd.DataFrame:
    out = df[[date_col, price_col]].copy()
    out.columns = list(out_cols)
    out[out_cols[0]] = pd.to_datetime(out[out_cols[0]], errors='coerce')
    out[out_cols[1]] = pd.to_numeric(out[out_cols[1]], errors='coerce')
    out = out.dropna().sort_values(out_cols[0]).drop_duplicates(out_cols[0])
    return out

# WTI daily data was pasted into NOTES.txt as CSV text.
wti_notes = RAW / 'uploaded_wti_daily_notes.txt'
wti = pd.read_csv(wti_notes)
wti = clean_date_price(wti, 'date', 'wti_usd_bbl', ('date', 'wti_usd_bbl'))
wti.to_csv(INTERIM / 'wti_daily.csv', index=False)

# WCS monthly data is in the file uploaded as wti.csv.
wcs_file = RAW / 'uploaded_wcs_monthly_misnamed_wti.csv'
wcs = pd.read_csv(wcs_file)
wcs = clean_date_price(wcs, 'date', 'wcs_usd_bbl', ('date', 'wcs_usd_bbl'))
wcs.to_csv(INTERIM / 'wcs_monthly.csv', index=False)

# AECO daily data is in the file uploaded as wcs.csv.
aeco_file = RAW / 'uploaded_aeco_daily_misnamed_wcs.csv'
aeco = pd.read_csv(aeco_file)
aeco = clean_date_price(aeco, 'date', 'aeco_cad_gj', ('date', 'aeco_cad_gj'))
aeco.to_csv(INTERIM / 'aeco_daily.csv', index=False)

# FactSet AECO export is an Excel workbook even though uploaded with .csv extension.
factset_file = RAW / 'uploaded_factset_aeco_excel_misnamed.csv'
try:
    fs = pd.read_excel(factset_file, sheet_name='Price History', header=None)
    # Row 1 contains labels: Date, Price, ...
    fs = fs.iloc[2:, [0, 1]].copy()
    fs.columns = ['date', 'aeco_factset_cad_gj']
    fs['date'] = pd.to_datetime(fs['date'], errors='coerce')
    fs['aeco_factset_cad_gj'] = pd.to_numeric(fs['aeco_factset_cad_gj'], errors='coerce')
    fs = fs.dropna().sort_values('date').drop_duplicates('date')
    fs.to_csv(INTERIM / 'factset_aeco_daily.csv', index=False)
except Exception as exc:
    print(f'Could not read FactSet Excel export: {exc}')

print('Extracted standardized price files to data/interim/')
print(f'WTI rows: {len(wti):,}, WCS rows: {len(wcs):,}, AECO rows: {len(aeco):,}')
