from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class CreateProductSchema(BaseModel):
    name: str
    price: Decimal

    description: Optional[str] = None
    stock: int = 0


class SearchProductSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
