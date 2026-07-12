from __future__ import annotations


def build_seller_message(model_label: str, offer: int) -> str:
    formatted_offer = f"${offer:,.0f}".replace(",", ".")
    return (
        f"Hola, ¿cómo estás? Vi el {model_label}. Me interesa porque estoy buscando cerrar esta semana, "
        f"pago contado y puedo hacer la transferencia rápido si está todo ok.\n\n"
        f"Considerando kilometraje, revisión y gastos para dejarlo listo, podría ofrecerte {formatted_offer}.\n\n"
        f"Si te acomoda, lo puedo ir a ver hoy o mañana."
    )
