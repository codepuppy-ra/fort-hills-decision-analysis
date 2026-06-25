# Methodology Notes

## Decision problem

Suncor must decide whether Fort Hills deserves additional marginal capital for productivity and cost-reduction improvements, or whether that capital should be redirected toward lower-cost assets.

## Empirical method

The repo uses a scenario-based managerial decision analysis:

1. Measure the oil price environment using WTI, WCS, and the WTI-WCS differential.
2. Estimate implied WCS as WTI minus the WTI-WCS differential.
3. Compare implied WCS to operating-cost scenarios.
4. Use margin per barrel to classify the recommended capital-allocation strategy.

## Formula

```text
margin_per_barrel = implied_wcs_usd_bbl - operating_cost_usd_bbl
implied_wcs_usd_bbl = wti_usd_bbl - wti_wcs_diff_usd_bbl
```

## Decision rule

```text
margin >= 35: Invest in productivity/cost reduction
20 <= margin < 35: Maintain and invest selectively
5 <= margin < 20: Limit new capital; fund only high-ROI cost controls
margin < 5: Redirect marginal capital / scale back discretionary spending
```

## Limitations

- WCS is a proxy for realized price, not an exact realized Fort Hills netback.
- The cost scenarios are placeholders until exact Fort Hills costs are collected from Suncor disclosures.
- The model does not include royalties, sustaining capex, taxes, transportation, hedging, depreciation, or full discounted cash-flow valuation.
- The purpose is managerial decision analysis, not engineering valuation.
