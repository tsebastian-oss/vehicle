from __future__ import annotations

import re


# Datos iniciales tomados de la conversación y del Excel Jan-Apr 2026.
# Reemplazar/expandir con data/transferencias.xlsx cuando se cargue el archivo real.
BASE_LIQUIDITY = {
    "chevrolet sail": {"transfers_jan_apr": 2460, "avg_monthly": 615, "score": 95},
    "kia morning": {"transfers_jan_apr": 2180, "avg_monthly": 545, "score": 90},
    "suzuki swift": {"transfers_jan_apr": 2277, "avg_monthly": 569, "score": 88},
    "hyundai grand i10": {"transfers_jan_apr": 1543, "avg_monthly": 386, "score": 82},
    "hyundai i10": {"transfers_jan_apr": 1543, "avg_monthly": 386, "score": 80},
    "suzuki baleno": {"transfers_jan_apr": 1234, "avg_monthly": 309, "score": 76},
    "peugeot 2008": {"transfers_jan_apr": 606, "avg_monthly": 152, "score": 55},
    "peugeot 208": {"transfers_jan_apr": 55, "avg_monthly": 14, "score": 42},
    "nissan x-trail e-power": {"transfers_jan_apr": 3, "avg_monthly": 0.75, "score": 22},
    "nissan xtrail epower": {"transfers_jan_apr": 3, "avg_monthly": 0.75, "score": 22},
    "nissan x-trail": {"transfers_jan_apr": 3, "avg_monthly": 0.75, "score": 24},
}


def normalize_name(value: str) -> str:
    value = value.lower().strip()
    value = value.replace("é", "e").replace("á", "a").replace("í", "i").replace("ó", "o").replace("ú", "u")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def get_liquidity_score(brand: str, model: str) -> float:
    key = normalize_name(f"{brand} {model}")

    for known_model, data in BASE_LIQUIDITY.items():
        normalized_known = normalize_name(known_model)
        if normalized_known in key or key in normalized_known:
            return float(data["score"])

    return 50.0
