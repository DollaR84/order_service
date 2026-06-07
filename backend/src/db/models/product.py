from decimal import Decimal
from typing import Optional, TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm as so

from ..base import Base
from ..mixins import TimeCreateMixin, TimeUpdateMixin


if TYPE_CHECKING:
    from .order import OrderItem


class Product(TimeCreateMixin, TimeUpdateMixin, Base):

    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)
    price: so.Mapped[Decimal] = so.mapped_column(sa.Numeric(10, 2), nullable=False)
    stock: so.Mapped[int] = so.mapped_column(nullable=False, default=0)

    order_items: so.Mapped[list["OrderItem"]] = so.relationship("OrderItem", back_populates="product")

    __table_args__ = (
        sa.CheckConstraint("stock >= 0", name="check_product_stock_positive"),
    )
