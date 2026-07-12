from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Transmission(str, Enum):
    manual = "manual"
    automatic = "automatic"
    unknown = "unknown"


class Fuel(str, Enum):
    gasoline = "gasoline"
    diesel = "diesel"
    hybrid = "hybrid"
    electric = "electric"
    unknown = "unknown"


class Comparable(BaseModel):
    title: str
    year: int
    km: int
    price: int
    region: str = "RM"
    url: Optional[str] = None


class Opportunity(BaseModel):
    brand: str = Field(..., examples=["Nissan"])
    model: str = Field(..., examples=["X-Trail e-POWER"])
    year: int = Field(..., examples=[2024])
    version: Optional[str] = Field(default=None, examples=["Advance"])
    km: int = Field(..., examples=[25000])
    price: int = Field(..., examples=[25000000])
    region: str = Field(default="RM")
    seller_type: str = Field(default="particular")
    transmission: Transmission = Transmission.unknown
    fuel: Fuel = Fuel.unknown
    owners: Optional[int] = None
    has_maintenance_records: bool = False
    has_fines: bool = False
    has_pledge: bool = False
    inspection_ok: bool = True
    notes: Optional[str] = None
    comparables: List[Comparable] = Field(default_factory=list)


class ScoreResult(BaseModel):
    liquidity_score: float
    margin_score: float
    market_discount_score: float
    km_score: float
    risk_score: float
    opportunity_score: float
    decision: str
    expected_sale_price: int
    fast_sale_price: int
    recommended_listing_price: int
    max_purchase_price: int
    initial_offer: int
    estimated_net_margin: int
    explanation: List[str]
    seller_message: str
