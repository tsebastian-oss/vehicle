# Reglas de negocio

## Meta inicial

Objetivo de utilidad: **$3.000.000 mensuales total**, equivalente a **$1.500.000 por socio**.

Modelo recomendado:

- 2 autos propios al mes con margen de $700.000 a $1.000.000 cada uno.
- 1 a 2 autos broker/consignación con comisión de $400.000 a $700.000 cada uno.

## Costos base

Para una evaluación conservadora se usa inicialmente:

| Ítem | Monto |
|---|---:|
| Transferencia / inscripción / impuesto | variable |
| Revisión / informe / scanner | $50.000 - $150.000 |
| Lavado / detailing básico | $80.000 - $180.000 |
| Publicación / pauta | $50.000 - $150.000 |
| Colchón comercial | $200.000 - $500.000 |

Para el MVP se usa `DEFAULT_COSTS = 430000`, que puede ajustarse por operación.

## Regla de compra

No comprar si no existe spread bruto mínimo:

| Tipo de auto | Spread bruto mínimo |
|---|---:|
| Auto chico líquido | $1.200.000 - $1.500.000 |
| Auto mediano | $1.500.000 - $2.000.000 |
| SUV / ticket alto | $2.500.000 - $3.500.000 |

## Regla de liquidez

La liquidez pesa mucho porque evita quedar atrapado con autos difíciles.

- Sail, Morning, Swift, Grand i10: alta liquidez.
- Peugeot 208 2017: liquidez baja-media.
- X-Trail e-POWER: baja liquidez; solo comprar si el margen es muy claro.

## Operación X-Trail e-POWER ejemplo

Caso conversado:

- Compra: $25.000.000
- Publicación: $27.990.000
- Transferencia aprox.: $425.000
- Utilidad si vende a publicación: aprox. $2.565.000
- Utilidad si cierra a $27.500.000: aprox. $2.075.000

Decisión: interesante si está impecable, con mantenciones Nissan, sin prenda, sin multas y garantía vigente.
