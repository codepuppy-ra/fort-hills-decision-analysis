from pathlib import Path

BASE = Path("data/manual")


def append_unique_rows(filename: str, rows: list[str]) -> None:
    path = BASE / filename
    existing = set()

    if path.exists():
        existing = set(line.strip() for line in path.read_text(encoding="utf-8").splitlines())

    with path.open("a", encoding="utf-8", newline="") as f:
        for row in rows:
            row = row.strip()
            if row and row not in existing:
                f.write(row + "\n")


append_unique_rows(
    "fort_hills_asset_facts.csv",
    [
        'fort_hills_slope_stability_issue,1,indicator,2021,S6,"Slope stability work at Fort Hills delayed the production ramp-up in 2021."',
        'fort_hills_open_pit_truck_shovel_mine,1,indicator,2021,S6,"Reuters describes Fort Hills as an open-pit truck and shovel mine."',
        'fort_hills_started_operating,2018,year,2018,S6,"Reuters notes Fort Hills started operating in 2018."',
    ],
)

append_unique_rows(
    "fort_hills_production_history.csv",
    [
        '2021,fort_hills_expected_output_low_after_delay,45,mbbls/d,S6,"Reuters reported expected 2021 Fort Hills output of 45000-55000 bpd after slope stability issue."',
        '2021,fort_hills_expected_output_high_after_delay,55,mbbls/d,S6,"Reuters reported expected 2021 Fort Hills output of 45000-55000 bpd after slope stability issue."',
        '2021,fort_hills_previous_output_guidance_low,65,mbbls/d,S6,"Reuters reported previous 2021 Fort Hills output guidance of 65000-85000 bpd."',
        '2021,fort_hills_previous_output_guidance_high,85,mbbls/d,S6,"Reuters reported previous 2021 Fort Hills output guidance of 65000-85000 bpd."',
    ],
)

append_unique_rows(
    "fort_hills_cash_operating_costs.csv",
    [
        '2021,Fort Hills,expected_cash_cost_low_after_delay,37,CAD/bbl,S6,"Reuters reported Fort Hills cash costs expected to rise to C$37-C$42/bbl in 2021 after slope stability work."',
        '2021,Fort Hills,expected_cash_cost_high_after_delay,42,CAD/bbl,S6,"Reuters reported Fort Hills cash costs expected to rise to C$37-C$42/bbl in 2021 after slope stability work."',
        '2021,Fort Hills,previous_cash_cost_guidance_low,25,CAD/bbl,S6,"Reuters reported previous Fort Hills 2021 cash cost guidance of C$25-C$29/bbl."',
        '2021,Fort Hills,previous_cash_cost_guidance_high,29,CAD/bbl,S6,"Reuters reported previous Fort Hills 2021 cash cost guidance of C$25-C$29/bbl."',
        '2024,Suncor Oil Sands Plants,operating_cost_range_low,28,CAD/bbl,S3,"Reuters/BOE reported operating costs at Suncor oil sands plants including Fort Hills and Syncrude ranged from C$28-C$38/bbl."',
        '2024,Suncor Oil Sands Plants,operating_cost_range_high,38,CAD/bbl,S3,"Reuters/BOE reported operating costs at Suncor oil sands plants including Fort Hills and Syncrude ranged from C$28-C$38/bbl."',
        '2024,Canadian Natural Resources Mining and Upgrading,operating_cost_comparison,22,CAD/bbl,S3,"Reuters/BOE reported Canadian Natural Resources mining and upgrading operating costs around C$22/bbl."',
    ],
)

append_unique_rows(
    "fort_hills_capex_strategy.csv",
    [
        '2024,cost_reduction_focus_oil_sands_mining,1,indicator,S3,"Reuters/BOE reported Suncor would focus on cutting operating costs in its oil sands mining business."',
        '2024,autonomous_haul_truck_fleet_target,91,vehicles,S3,"Reuters/BOE reported Suncor planned to double its autonomous haul truck fleet to 91 vehicles."',
        '2024,savings_per_autonomous_truck_conversion,1,CAD millions per truck per year,S3,"Reuters/BOE reported each autonomous truck conversion saves about C$1 million per truck per year."',
        '2026,suncor_upstream_production_guidance_low,840,mbbls/d,S4,"Reuters reported Suncor expects upstream production of 840000-870000 bpd in 2026."',
        '2026,suncor_upstream_production_guidance_high,870,mbbls/d,S4,"Reuters reported Suncor expects upstream production of 840000-870000 bpd in 2026."',
        '2026,suncor_capex_guidance_low,5600,CAD millions,S4,"Reuters reported Suncor expects 2026 capital expenditure of C$5.6-C$5.8 billion."',
        '2026,suncor_capex_guidance_high,5800,CAD millions,S4,"Reuters reported Suncor expects 2026 capital expenditure of C$5.6-C$5.8 billion."',
        '2025,suncor_capex_forecast_low,6100,CAD millions,S4,"Reuters reported Suncor 2025 forecast capex range was C$6.1-C$6.3 billion."',
        '2025,suncor_capex_forecast_high,6300,CAD millions,S4,"Reuters reported Suncor 2025 forecast capex range was C$6.1-C$6.3 billion."',
        '2026,fort_hills_north_pit_major_investment,1,indicator,S4,"Reuters reported major 2026 investments include Fort Hills North Pit."',
        '2026,monthly_share_buybacks,275,CAD millions,S4,"Reuters reported Suncor increased monthly share buybacks to C$275 million."',
        '2026,annualized_share_buybacks,3300,CAD millions,S4,"Reuters reported monthly buybacks point to C$3.3 billion in repurchases next year."',
    ],
)

print("External manual data rows added successfully.")