from __future__ import annotations

from statistics import median

from backend.liquidity import get_liquidity_score
from backend.messages import build_seller_message
from backend.models import Opportunity, ScoreResult

DEFAULT_COSTS = 430_000
DEFAULT_TARGET_MARGIN = 800_000

HIGH_RISK_KEYWORDS = [
    "bmw",
    "mercedes",
    "audi",
    "fiesta automatic",
    "focus automatic",
    "cruze",
]


def clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def calculate_market_prices(opportunity: Opportunity) -> tuple[int, int, int]:
    if opportunity.comparables:
        prices = sorted([c.price for c in opportunity.comparables])
        med = int(median(prices))
        fast_sale = int(med * 0.94)
        listing = int(med * 1.02)
        return med, fast_sale, listing

    # Fallback cuando no hay comparables: se asume que el precio publicado actual es 93% del precio esperado.
    expected_sale = int(opportunity.price / 0.93)
    fast_sale = int(expected_sale * 0.94)
    listing = int(expected_sale * 1.02)
    return expected_sale, fast_sale, listing


def calculate_km_score(year: int, km: int) -> float:
    # Regla simple: 15.000 km/año es normal para Chile.
    from datetime import date

    age = max(1, date.today().year - year + 1)
    expected_km = age * 15_000
    ratio = km / expected_km

    if ratio <= 0.75:
        return 100
    if ratio <= 1.0:
        return 85
    if ratio <= 1.3:
        return 65
    if ratio <= 1.6:
        return 45
    return 25


def calculate_risk_score(opportunity: Opportunity) -> float:
    label = f"{opportunity.brand} {opportunity.model} {opportunity.version or ''}".lower()
    score = 90.0

    if any(keyword in label for keyword in HIGH_RISK_KEYWORDS):
        score -= 35
    if opportunity.has_fines:
        score -= 25
    if opportunity.has_pledge:
        score -= 50
    if not opportunity.inspection_ok:
        score -= 30
    if opportunity.owners and opportunity.owners > 3:
        score -= 15
    if not opportunity.has_maintenance_records and opportunity.price >= 15_000_000:
        score -= 12

    return clamp(score)


def score_opportunity(
    opportunity: Opportunity,
    costs: int = DEFAULT_COSTS,
    target_margin: int = DEFAULT_TARGET_MARGIN,
) -> ScoreResult:
    expected_sale_price, fast_sale_price, listing_price = calculate_market_prices(opportunity)
    max_purchase_price = fast_sale_price - costs - target_margin
    initial_offer = int(max_purchase_price * 0.96)
    estimated_net_margin = fast_sale_price - opportunity.price - costs

    liquidity_score = get_liquidity_score(opportunity.brand, opportunity.model)

    margin_ratio = estimated_net_margin / max(target_margin, 1)
    margin_score = clamp(margin_ratio * 100)

    market_discount = (expected_sale_price - opportunity.price) / max(expected_sale_price, 1)
    market_discount_score = clamp(market_discount * 500)  # 20% bajo mercado ~= 100 puntos

    km_score = calculate_km_score(opportunity.year, opportunity.km)
    risk_score = calculate_risk_score(opportunity)

    opportunity_score = round(
        margin_score * 0.35
        + liquidity_score * 0.25
        + market_discount_score * 0.20
        + km_score * 0.10
        + risk_score * 0.10,
        1,
    )

    if opportunity.has_pledge or opportunity.has_fines or not opportunity.inspection_ok:
        decision = "DESCARTAR"
    elif opportunity_score >= 85 and estimated_net_margin >= target_margin:
        decision = "COMPRAR / LLAMAR HOY"
    elif opportunity_score >= 70:
        decision = "NEGOCIAR"
    elif opportunity_score >= 55:
        decision = "MONITOREAR"
    else:
        decision = "DESCARTAR"

    label = " ".join(
        str(x)
        for x in [opportunity.brand, opportunity.model, opportunity.year, opportunity.version]
        if x
    )

    explanation = [
        f"Liquidez modelo: {liquidity_score:.0f}/100.",
        f"Venta rápida estimada: ${fast_sale_price:,.0f}".replace(",", "."),
        f"Precio máximo de compra recomendado: ${max_purchase_price:,.0f}".replace(",", "."),
        f"Margen neto estimado al precio actual: ${estimated_net_margin:,.0f}".replace(",", "."),
    ]

    if liquidity_score < 40:
        explanation.append("Ojo: modelo de baja rotación; comprar solo si el margen es muy claro.")
    if estimated_net_margin < target_margin:
        explanation.append("El margen no alcanza el objetivo; requiere negociar más abajo.")

    return ScoreResult(
        liquidity_score=liquidity_score,
        margin_score=round(margin_score, 1),
        market_discount_score=round(market_discount_score, 1),
        km_score=round(km_score, 1),
        risk_score=round(risk_score, 1),
        opportunity_score=opportunity_score,
        decision=decision,
        expected_sale_price=expected_sale_price,
        fast_sale_price=fast_sale_price,
        recommended_listing_price=listing_price,
        max_purchase_price=max_purchase_price,
        initial_offer=initial_offer,
        estimated_net_margin=estimated_net_margin,
        explanation=explanation,
        seller_message=build_seller_message(label, initial_offer),
    )
