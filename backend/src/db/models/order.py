from decimal import Decimal
from typing import TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm as so

from application.types import OrderStatusType

from ..base import Base
from ..mixins import TimeCreateMixin, TimeUpdateMixin


if TYPE_CHECKING:
    from .client import Client
    from .product import Product


class Order(TimeCreateMixin, TimeUpdateMixin, Base):

    total_price: so.Mapped[Decimal] = so.mapped_column(sa.Numeric(10, 2), nullable=False)
    status: so.Mapped[OrderStatusType] = so.mapped_column(
        sa.Enum(OrderStatusType, name="order_status_type", create_constraint=True, validate_strings=True),
        default=OrderStatusType.PENDING,
        nullable=False,
        index=True,
    )

    client_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("clients.id", ondelete="CASCADE"), index=True)
    client: so.Mapped["Client"] = so.relationship("Client", back_populates="orders")

    items: so.Mapped[list["OrderItem"]] = so.relationship(
        "OrderItem", back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class OrderItem(TimeCreateMixin, Base):

    order_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    product_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("products.id"), index=True)

    quantity: so.Mapped[int] = so.mapped_column(nullable=False, default=1)
    price_at_time: so.Mapped[Decimal] = so.mapped_column(sa.Numeric(10, 2), nullable=False)

    order: so.Mapped["Order"] = so.relationship("Order", back_populates="items")
    product: so.Mapped["Product"] = so.relationship("Product", back_populates="order_items")

    __table_args__ = (
        sa.CheckConstraint("quantity > 0", name="check_order_item_quantity_positive"),
    )
