# Suncor Fort Hills Managerial Economics Analysis

This repository builds a firm-level decision analysis for Suncor's Fort Hills asset.

**Managerial question**

> Should Suncor continue investing in Fort Hills productivity/cost-reduction improvements, maintain the asset with selective spending, or redirect marginal capital elsewhere under WTI/WCS price uncertainty?

The repository cleans the uploaded commodity-price files, builds annual/monthly WTI-WCS price measures, and produces a scenario-based margin and decision model.

## Repo structure

```text
src/
  01_extract_uploaded_prices.py   # Reads uploaded raw files, including misnamed files
  02_clean_price_panel.py         # Monthly/annual WTI, WCS, differential, AECO
  03_fort_hills_decision_model.py # Scenario and margin analysis
  04_build_figures.py             # Charts for the paper

data/raw/       # Uploaded raw files copied here

data/cleaned/   # Clean price panel + assumptions
outputs/tables/ # Decision/scenario tables
outputs/figures/# Paper-ready figures
```

## Quick start

```bash
pip install -r requirements.txt
python src/01_extract_uploaded_prices.py
python src/02_clean_price_panel.py
python src/03_fort_hills_decision_model.py
python src/04_build_figures.py
```

Or run everything:

```bash
python run_pipeline.py
```

## What the analysis does

1. **Extracts price data** from the uploaded files.
   - WTI daily data is read from `uploaded_wti_daily_notes.txt`.
   - WCS monthly data is read from `uploaded_wcs_monthly_misnamed_wti.csv`.
   - AECO daily data is read from `uploaded_aeco_daily_misnamed_wcs.csv`.
   - The FactSet Excel export is read from `uploaded_factset_aeco_excel_misnamed.csv` even though the extension is `.csv`.

2. **Builds a cleaned price panel**.
   - Converts daily WTI/AECO to monthly and annual averages.
   - Merges WTI and WCS by month.
   - Computes `wti_wcs_diff_usd_bbl = wti_usd_bbl - wcs_usd_bbl`.

3. **Runs a Fort Hills decision model**.
   - Uses price scenarios based on recent historical quantiles.
   - Uses operating-cost scenarios to model cost reduction.
   - Computes approximate margin per barrel:

```text
margin_per_bbl = implied_wcs_usd_bbl - operating_cost_usd_bbl
```

4. **Outputs managerial recommendations**.
   - Invest in cost reductions.
   - Maintain/selective investment.
   - Limit new capital.
   - Redirect marginal capital.

## How to interpret the model

This is not a full discounted cash-flow or reserve-engineering model. It is a managerial economics decision analysis. The point is to show how commodity-price uncertainty and cost performance change the rational capital-allocation decision.

The decision rule is deliberately transparent:

```text
margin >= 35: Invest in productivity/cost reduction
20 <= margin < 35: Maintain and invest selectively
5 <= margin < 20: Limit new capital; only fund high-ROI cost controls
margin < 5: Redirect marginal capital / scale back discretionary spending
```

## Main outputs

```text
data/cleaned/monthly_price_panel.csv
outputs/tables/fort_hills_scenario_results.csv
outputs/tables/fort_hills_decision_summary.csv
outputs/figures/wti_wcs_monthly.png
outputs/figures/wti_wcs_differential.png
outputs/figures/fort_hills_margin_scenarios.png
```

## Paper framing

Use this as the paper's central claim:

> Suncor should continue investing in Fort Hills only if the investment directly lowers operating costs or improves utilization. The case for continued investment is strongest when WTI is moderate-to-high, the WCS differential is narrow-to-moderate, and cost-reduction investments lower Fort Hills' per-barrel cost enough to protect margins. If the WCS differential widens or costs remain elevated, Suncor should limit discretionary Fort Hills capital and redirect marginal capital toward lower-cost assets.
