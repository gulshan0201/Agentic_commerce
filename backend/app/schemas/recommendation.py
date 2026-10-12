from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    category_id: int

    budget_max: Decimal = Field(
        gt=0
    )

    use_case: str | None = None

    minimum_ram: int | None = Field(
        default=None,
        ge=1
    )

    gpu_required: bool = False

    minimum_rating: float | None = Field(
        default=None,
        ge=0,
        le=5
    )

    in_stock_only: bool = True


class RecommendationItem(BaseModel):
    product_id: int

    name: str

    brand: str | None

    price: Decimal

    match_score: float

    reasons: list[str]

    specifications: dict[str, Any] | None = None


class RecommendationResponse(BaseModel):
    total_matches: int

    recommendations: list[RecommendationItem]