"""Fort Hills scenario decision model.

This model uses WTI/WCS price scenarios and Suncor-reported Fort Hills cash
operating costs to evaluate whether Suncor should continue productivity-focused
investment, invest selectively, or redirect marginal capital.
"""

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "cleaned"
MANUAL = ROOT / "data" / "manual"
OUT = ROOT / "outputs" / "tables"

OUT.mkdir(parents=True, exist_ok=True)
CLEAN.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return pd.read_csv(path)


def get_assumption(assumptions: pd.DataFrame, name: str, default: float | None = None) -> float:
    row = assumptions.loc[assumptions["assumption"] == name]

    if row.empty:
        if default is not None:
            return float(default)
        raise ValueError(f"Missing assumption: {name}")

    return float(row.iloc[0]["value"])


def recommend(margin_cad_bbl: float, continue_threshold: float, selective_threshold: float) -> str:
    if margin_cad_bbl >= continue_threshold:
        return "Continue productivity-focused Fort Hills investment"
    if margin_cad_bbl >= selective_threshold:
        return "Maintain selective/discipline-focused investment"
    if margin_cad_bbl > 0:
        return "Limit new capital; focus on maintenance and cost control"
    return "Redirect marginal capital away from Fort Hills"


def main() -> None:
    price_scenarios = read_csv(CLEAN / "price_scenarios_from_2015_quantiles.csv")
    assumptions = read_csv(MANUAL / "fort_hills_decision_assumptions.csv")

    base_cost = get_assumption(assumptions, "base_fort_hills_cash_cost")
    improved_cost = get_assumption(assumptions, "improved_cost_case")
    stressed_cost = get_assumption(assumptions, "stressed_cost_case")

    continue_threshold = get_assumption(
        assumptions,
        "continue_investment_margin_threshold",
    )
    selective_threshold = get_assumption(
        assumptions,
        "selective_investment_margin_threshold",
    )

    # Default FX rate. You can later replace this with a proper annual FX series.
    usd_to_cad = get_assumption(
        assumptions,
        "usd_to_cad_exchange_rate",
        default=1.37,
    )

    if "scenario" not in price_scenarios.columns:
        price_scenarios["scenario"] = [f"scenario_{i + 1}" for i in range(len(price_scenarios))]

    if "implied_wcs_usd_bbl" not in price_scenarios.columns:
        raise ValueError(
            "Expected price_scenarios_from_2015_quantiles.csv to contain "
            "'implied_wcs_usd_bbl'. Available columns are: "
            f"{list(price_scenarios.columns)}"
        )

    price_scenarios["implied_wcs_cad_bbl"] = (
        price_scenarios["implied_wcs_usd_bbl"] * usd_to_cad
    )

    cost_scenarios = pd.DataFrame(
        [
            {
                "cost_case": "Improved cost case",
                "cash_operating_cost_cad_bbl": improved_cost,
                "source": "Q4 2025 Fort Hills total cash operating cost",
            },
            {
                "cost_case": "Base cost case",
                "cash_operating_cost_cad_bbl": base_cost,
                "source": "FY 2025 Fort Hills total cash operating cost",
            },
            {
                "cost_case": "Stressed cost case",
                "cash_operating_cost_cad_bbl": stressed_cost,
                "source": "Q2 2025 Fort Hills total cash operating cost",
            },
        ]
    )

    results = price_scenarios.merge(cost_scenarios, how="cross")

    results["margin_cad_bbl"] = (
        results["implied_wcs_cad_bbl"] - results["cash_operating_cost_cad_bbl"]
    )

    results["decision_recommendation"] = results["margin_cad_bbl"].apply(
        lambda margin: recommend(margin, continue_threshold, selective_threshold)
    )

    results["investment_attractiveness_score"] = np.clip(
        (results["margin_cad_bbl"] + 10) / 70 * 100,
        0,
        100,
    )

    results_out = results[
        [
            "scenario",
            "wti_usd_bbl",
            "wti_wcs_diff_usd_bbl",
            "implied_wcs_usd_bbl",
            "implied_wcs_cad_bbl",
            "cost_case",
            "cash_operating_cost_cad_bbl",
            "margin_cad_bbl",
            "investment_attractiveness_score",
            "decision_recommendation",
        ]
    ].copy()

    summary = results_out.groupby("scenario", as_index=False).agg(
        avg_margin_cad_bbl=("margin_cad_bbl", "mean"),
        min_margin_cad_bbl=("margin_cad_bbl", "min"),
        max_margin_cad_bbl=("margin_cad_bbl", "max"),
        avg_investment_score=("investment_attractiveness_score", "mean"),
    )

    summary["managerial_interpretation"] = summary["avg_margin_cad_bbl"].apply(
        lambda margin: recommend(margin, continue_threshold, selective_threshold)
    )

    results_out.to_csv(OUT / "fort_hills_scenario_results.csv", index=False)
    summary.to_csv(OUT / "fort_hills_decision_summary.csv", index=False)
    cost_scenarios.to_csv(CLEAN / "fort_hills_cost_scenarios.csv", index=False)

    print("Built Fort Hills scenario model using manual Fort Hills cost assumptions.")
    print(results_out)


if __name__ == "__main__":
    main()