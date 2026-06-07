from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from .base import BaseData


@dataclass(slots=True, kw_only=True)
class BaseProduct(BaseData):
    name: str
    description: Optional[str] = None

    price: Decimal
    stock: int = 0


@dataclass(slots=True, kw_only=True)
class NewProduct(BaseProduct):
    pass


@dataclass(slots=True)
class Product(BaseProduct):
    id: int

    created_at: datetime
    updated_at: datetime
