# Methodology Notes

## Decision problem

This project analyzes Suncor’s Fort Hills oil sands asset as a firm-level capital allocation problem. Suncor must decide whether Fort Hills deserves additional marginal capital for productivity, capacity, and cost-reduction improvements, or whether that capital should be redirected toward lower-cost assets or shareholder returns.

The decision is treated as a managerial economics problem rather than a full engineering valuation. The focus is on how Fort Hills’ operating-cost position interacts with WTI/WCS price uncertainty.

## Empirical method

The repo uses a scenario-based managerial decision analysis.

1. Measure the oil price environment using WTI, WCS, and the WTI-WCS differential.
2. Estimate implied WCS as WTI minus the WTI-WCS differential.
3. Convert implied WCS from USD per barrel into CAD per barrel using a stated exchange-rate assumption.
4. Compare implied WCS in CAD per barrel with Suncor-reported Fort Hills cash operating cost scenarios.
5. Use margin per barrel to classify the recommended capital-allocation strategy.

The model uses WTI/WCS price scenarios based on the distribution of monthly prices from 2015 onward. Fort Hills cost scenarios are based on Suncor-reported Fort Hills cash operating costs, including the 2025 annual average, the Q4 2025 improved-cost case, and the Q2 2025 stressed-cost case.

## Key formulas

```text
implied_wcs_usd_bbl = wti_usd_bbl - wti_wcs_diff_usd_bbl

implied_wcs_cad_bbl = implied_wcs_usd_bbl × usd_to_cad_exchange_rate

margin_cad_bbl = implied_wcs_cad_bbl - fort_hills_cash_operating_cost_cad_bbl
```

## Cost scenarios

```text
Improved cost case: Q4 2025 Fort Hills total cash operating cost per barrel
Base cost case: FY 2025 Fort Hills total cash operating cost per barrel
Stressed cost case: Q2 2025 Fort Hills total cash operating cost per barrel
```

These cost cases are intended to show how the recommendation changes if Fort Hills performs closer to its stronger quarterly cost performance versus a weaker quarterly cost environment.

## Decision rule

```text
margin >= 20 CAD/bbl:
    Continue productivity-focused Fort Hills investment

10 <= margin < 20 CAD/bbl:
    Maintain selective or discipline-focused investment

0 < margin < 10 CAD/bbl:
    Limit new capital; focus on maintenance and cost control

margin <= 0 CAD/bbl:
    Redirect marginal capital away from Fort Hills
```

The thresholds are not engineering break-even values. They are transparent managerial decision thresholds used to classify whether Fort Hills appears attractive under different price and cost scenarios.

## Source structure

The manual data files use source IDs to keep the analysis traceable.

```text
S1 = Suncor Fort Hills asset page
S2 = Suncor Energy Annual Report 2025
S3 = Reuters/BOE operating cost article
S4 = Reuters 2026 Suncor guidance article
S5 = Suncor Q4 2025 operating summary
S6 = Reuters 2021 Fort Hills ramp-up delay article
```

Company disclosures are used for Fort Hills production, cash operating costs, price realizations, segment financials, and capital spending. External Reuters/BOE sources are used to motivate the cost-reduction problem, peer cost comparison, 2026 capital guidance, and Fort Hills’ earlier operating challenges.

## Interpretation

The model is designed to answer whether continued Fort Hills investment remains attractive under price and cost uncertainty.

If margins remain strong across price and cost scenarios, continued productivity-focused investment is more defensible. If margins weaken materially under low-price or stressed-cost scenarios, Suncor should be more selective and may prefer maintenance discipline, targeted cost control, or redirecting marginal capital elsewhere.

## Limitations

* WCS is a proxy for realized price, not an exact Fort Hills realized netback.
* The model uses a simplified exchange-rate assumption to compare USD oil prices with CAD operating costs.
* The model does not include royalties, sustaining capex, taxes, transportation, hedging, depreciation, or full discounted cash-flow valuation.
* The model does not estimate project-level net present value.
* The purpose is managerial decision analysis, not engineering valuation.
