from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from .base import BaseData


@dataclass(slots=True, kw_only=True)
class BaseProductModel(BaseData):
    name: str
    description: Optional[str] = None

    stock: int = 0
    price: Decimal


@dataclass(slots=True, kw_only=True)
class NewProductModel(BaseProductModel):
    pass


@dataclass(slots=True)
class ProductModel(BaseProductModel):
    id: int

    created_at: datetime
    updated_at: datetime
