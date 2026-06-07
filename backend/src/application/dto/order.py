from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from application.types import OrderStatusType

from .base import BaseData


@dataclass(slots=True, kw_only=True)
class BaseOrderItem(BaseData):
    product_id: int
    quantity: int = 1


@dataclass(slots=True, kw_only=True)
class NewOrderItem(BaseOrderItem):
    pass


@dataclass(slots=True)
class OrderItem(BaseOrderItem):
    id: int
    order_id: int
    price_at_time: Decimal

    created_at: datetime


@dataclass(slots=True, kw_only=True)
class BaseOrder(BaseData):
    client_id: int
    status: OrderStatusType = OrderStatusType.PENDING


@dataclass(slots=True, kw_only=True)
class NewOrder(BaseOrder):
    items: list[NewOrderItem] = field(default_factory=list)


@dataclass(slots=True)
class Order(BaseOrder):
    id: int
    total_price: Decimal

    created_at: datetime
    updated_at: datetime

    items: list[OrderItem] = field(default_factory=list)
