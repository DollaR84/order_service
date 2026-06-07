from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from application.types import OrderStatusType

from .base import BaseData


@dataclass(slots=True, kw_only=True)
class BaseOrderItemModel(BaseData):
    product_id: int
    quantity: int = 1


@dataclass(slots=True, kw_only=True)
class NewOrderItemModel(BaseOrderItemModel):
    pass


@dataclass(slots=True)
class OrderItemModel(BaseOrderItemModel):
    id: int
    order_id: int
    created_at: datetime
    price_at_time: Decimal


@dataclass(slots=True, kw_only=True)
class BaseOrderModel(BaseData):
    client_id: int
    status: OrderStatusType = OrderStatusType.PENDING


@dataclass(slots=True, kw_only=True)
class NewOrderModel(BaseOrderModel):
    items: list[NewOrderItemModel] = field(default_factory=list)


@dataclass(slots=True)
class OrderModel(BaseOrderModel):
    id: int
    total_price: Decimal

    created_at: datetime
    updated_at: datetime

    items: list[OrderItemModel] = field(default_factory=list)
