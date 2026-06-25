"""Fort Hills scenario decision model.

This is intentionally transparent for a managerial economics paper. It models how the
recommendation changes under WTI/WCS price scenarios and operating-cost scenarios.
"""
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / 'data' / 'cleaned'
OUT = ROOT / 'outputs' / 'tables'
OUT.mkdir(parents=True, exist_ok=True)

panel = pd.read_csv(CLEAN / 'monthly_price_panel.csv', parse_dates=['month'])
recent = panel[(panel['month'] >= '2015-01-01') & panel['wti_usd_bbl'].notna() & panel['wcs_usd_bbl'].notna()].copy()

# Scenario values are based on quantiles of the 2015+ monthly data.
def q(series, pct):
    return float(series.quantile(pct))

scenario_rows = [
    {'scenario': 'Low price / wide differential',
     'wti_usd_bbl': q(recent['wti_usd_bbl'], 0.25),
     'wti_wcs_diff_usd_bbl': q(recent['wti_wcs_diff_usd_bbl'], 0.75)},
    {'scenario': 'Base case',
     'wti_usd_bbl': q(recent['wti_usd_bbl'], 0.50),
     'wti_wcs_diff_usd_bbl': q(recent['wti_wcs_diff_usd_bbl'], 0.50)},
    {'scenario': 'High price / moderate differential',
     'wti_usd_bbl': q(recent['wti_usd_bbl'], 0.75),
     'wti_wcs_diff_usd_bbl': q(recent['wti_wcs_diff_usd_bbl'], 0.50)},
    {'scenario': 'Boom price / narrow differential',
     'wti_usd_bbl': q(recent['wti_usd_bbl'], 0.90),
     'wti_wcs_diff_usd_bbl': q(recent['wti_wcs_diff_usd_bbl'], 0.25)},
]
scenarios = pd.DataFrame(scenario_rows)
scenarios['implied_wcs_usd_bbl'] = scenarios['wti_usd_bbl'] - scenarios['wti_wcs_diff_usd_bbl']

# Replace these with Fort Hills/Suncor-reported costs if you collect exact values.
# USD/bbl used for consistency with WTI/WCS. If costs are CAD/bbl, add FX conversion.
cost_scenarios = pd.DataFrame([
    {'cost_case': 'High/current cost', 'operating_cost_usd_bbl': 38.0},
    {'cost_case': 'Moderate improvement', 'operating_cost_usd_bbl': 34.0},
    {'cost_case': 'Strong improvement', 'operating_cost_usd_bbl': 30.0},
])

results = scenarios.merge(cost_scenarios, how='cross')
results['margin_usd_bbl'] = results['implied_wcs_usd_bbl'] - results['operating_cost_usd_bbl']


def recommend(margin: float) -> str:
    if margin >= 35:
        return 'Invest in productivity/cost reduction'
    if margin >= 20:
        return 'Maintain and invest selectively'
    if margin >= 5:
        return 'Limit new capital; fund only high-ROI cost controls'
    return 'Redirect marginal capital / scale back discretionary spending'

results['decision_recommendation'] = results['margin_usd_bbl'].apply(recommend)

# Add a compact score for sorting/plotting. Higher = more attractive.
results['investment_attractiveness_score'] = np.clip((results['margin_usd_bbl'] + 10) / 60 * 100, 0, 100)

results.to_csv(OUT / 'fort_hills_scenario_results.csv', index=False)

summary = results.groupby('scenario', as_index=False).agg(
    avg_margin_usd_bbl=('margin_usd_bbl', 'mean'),
    min_margin_usd_bbl=('margin_usd_bbl', 'min'),
    max_margin_usd_bbl=('margin_usd_bbl', 'max'),
    avg_investment_score=('investment_attractiveness_score', 'mean')
)
summary['managerial_interpretation'] = summary['avg_margin_usd_bbl'].apply(recommend)
summary.to_csv(OUT / 'fort_hills_decision_summary.csv', index=False)

scenarios.to_csv(CLEAN / 'price_scenarios_from_2015_quantiles.csv', index=False)
cost_scenarios.to_csv(CLEAN / 'fort_hills_cost_scenarios.csv', index=False)

print('Built Fort Hills scenario model.')
print(results[['scenario','cost_case','implied_wcs_usd_bbl','operating_cost_usd_bbl','margin_usd_bbl','decision_recommendation']])
