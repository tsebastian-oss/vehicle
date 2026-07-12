from fastapi import FastAPI

from backend.models import Opportunity, ScoreResult
from backend.scoring import score_opportunity

app = FastAPI(
    title="MGP Auto Scout Agent",
    description="Agente para evaluar oportunidades de compra/venta de autos usados en Chile.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "MGP Auto Scout Agent",
        "status": "ok",
        "docs": "/docs",
    }


@app.post("/score", response_model=ScoreResult)
def score(opportunity: Opportunity):
    return score_opportunity(opportunity)


@app.get("/health")
def health():
    return {"status": "healthy"}
