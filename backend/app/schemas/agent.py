from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field


class AgentMessageRequest(BaseModel):
    message: str = Field(
        min_length=2,
        max_length=1000
    )


class ProductSummary(BaseModel):
    id: int
    name: str
    brand: str | None = None
    price: Decimal
    stock: int
    rating: float | None = None
    specifications: dict[str, Any] | None = None


class ProductComparisonRequest(BaseModel):
    product_ids: list[int] = Field(
        min_length=2,
        max_length=5
    )


class StockCheckResponse(BaseModel):
    product_id: int
    name: str
    stock: int
    available: bool