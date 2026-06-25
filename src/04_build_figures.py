"""Build paper-ready figures."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / 'data' / 'cleaned'
TABLES = ROOT / 'outputs' / 'tables'
FIG = ROOT / 'outputs' / 'figures'
FIG.mkdir(parents=True, exist_ok=True)

panel = pd.read_csv(CLEAN / 'monthly_price_panel.csv', parse_dates=['month'])
plot_panel = panel[panel['month'] >= '2005-01-01'].copy()

# Figure 1: WTI and WCS
plt.figure(figsize=(10, 5))
plt.plot(plot_panel['month'], plot_panel['wti_usd_bbl'], label='WTI')
plt.plot(plot_panel['month'], plot_panel['wcs_usd_bbl'], label='WCS')
plt.title('WTI and WCS Monthly Prices')
plt.xlabel('Year')
plt.ylabel('USD per barrel')
plt.legend()
plt.tight_layout()
plt.savefig(FIG / 'wti_wcs_monthly.png', dpi=200)
plt.close()

# Figure 2: WTI-WCS differential
plt.figure(figsize=(10, 5))
plt.plot(plot_panel['month'], plot_panel['wti_wcs_diff_usd_bbl'])
plt.title('WTI-WCS Differential')
plt.xlabel('Year')
plt.ylabel('USD per barrel')
plt.tight_layout()
plt.savefig(FIG / 'wti_wcs_differential.png', dpi=200)
plt.close()

# Figure 3: Fort Hills margin scenarios
res = pd.read_csv(TABLES / 'fort_hills_scenario_results.csv')
pivot = res.pivot(index='scenario', columns='cost_case', values='margin_usd_bbl')
# Preserve scenario order in CSV
scenario_order = res['scenario'].drop_duplicates().tolist()
pivot = pivot.loc[scenario_order]
ax = pivot.plot(kind='bar', figsize=(11, 6))
ax.set_title('Fort Hills Approximate Margin by Price and Cost Scenario')
ax.set_xlabel('Price scenario')
ax.set_ylabel('Margin, USD per barrel')
plt.xticks(rotation=25, ha='right')
plt.tight_layout()
plt.savefig(FIG / 'fort_hills_margin_scenarios.png', dpi=200)
plt.close()

print('Built figures in outputs/figures/')
