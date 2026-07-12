# MGP Auto Scout Agent

Agente para detectar oportunidades de compra/venta de autos usados en Chile, usando liquidez de transferencias, comparables de mercado y reglas de negocio.

## Objetivo

Ayudar a Sebastián y su socio a decidir rápido si un auto conviene:

- **Comprar** si el margen y la liquidez son fuertes.
- **Negociar** si el precio está cerca, pero falta descuento.
- **Monitorear** si el caso es interesante pero aún no da.
- **Descartar** si el riesgo, la baja rotación o el margen no justifican la operación.

## MVP actual

Este repositorio parte con un MVP semi-manual:

1. Cargas o registras una oportunidad.
2. Ingresas datos del auto y comparables manuales.
3. El agente calcula liquidez, margen, precio máximo de compra, oferta inicial y score.
4. Devuelve decisión y mensaje sugerido para contactar al vendedor.

El scraping automático de Chileautos debe agregarse después y con cuidado, para evitar bloqueos y datos incompletos.

## Modelos objetivo iniciales

### Rotación rápida

- Chevrolet Sail 2016-2018
- Hyundai Grand i10 2016-2018
- Kia Morning 2016-2019
- Suzuki Swift 2014-2017
- Hyundai Accent 2014-2016
- Kia Rio 2014-2016
- Nissan Versa 2014-2016
- Toyota Yaris 2013-2016

### Oportunidades de margen alto

- Nissan X-Trail e-POWER 2023-2024
- Toyota RAV4 2012-2016
- Suzuki Vitara 2016-2018
- Hyundai Tucson 2016-2018
- Kia Sportage 2015-2017
- Nissan Kicks 2017-2019

## Fórmula base

```text
margen_neto = precio_venta_esperado - precio_compra - costos
precio_maximo_compra = precio_venta_rapida - costos - margen_objetivo
```

## Score

| Factor | Peso |
|---|---:|
| Margen estimado | 35% |
| Liquidez según transferencias | 25% |
| Precio bajo mercado | 20% |
| Kilometraje | 10% |
| Riesgo del modelo | 10% |

## Decisiones

| Score | Acción |
|---:|---|
| 85-100 | Comprar / llamar hoy |
| 70-84 | Negociar |
| 55-69 | Monitorear |
| <55 | Descartar |

## Instalación local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Luego abre:

```text
http://127.0.0.1:8000/docs
```

## Próximos pasos

- Cargar el Excel real de transferencias en `data/transferencias.xlsx`.
- Ajustar liquidez por modelo según el Excel.
- Crear frontend simple.
- Agregar CRM de oportunidades.
- Agregar scanner semi-automático de links de Chileautos.
