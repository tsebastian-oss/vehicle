from backend.models import Comparable, Fuel, Opportunity, Transmission
from backend.scoring import score_opportunity


if __name__ == "__main__":
    opportunity = Opportunity(
        brand="Nissan",
        model="X-Trail e-POWER",
        year=2024,
        version="Advance",
        km=25000,
        price=25000000,
        region="RM",
        seller_type="known_owner",
        transmission=Transmission.automatic,
        fuel=Fuel.hybrid,
        has_maintenance_records=True,
        has_fines=False,
        has_pledge=False,
        inspection_ok=True,
        comparables=[
            Comparable(title="X-Trail e-POWER Advance 2024", year=2024, km=12000, price=30900000, region="RM"),
            Comparable(title="X-Trail e-POWER Advance 2024", year=2024, km=79385, price=28790000, region="RM"),
            Comparable(title="X-Trail e-POWER Advance 2023", year=2023, km=45000, price=26900000, region="RM"),
        ],
    )

    result = score_opportunity(opportunity, costs=425000, target_margin=1500000)
    print(result.model_dump_json(indent=2))
