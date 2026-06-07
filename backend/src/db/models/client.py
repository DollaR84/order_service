from typing import Optional, TYPE_CHECKING
import uuid

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.dialects.postgresql import UUID as PgUUID

from ..base import Base
from ..mixins import TimeCreateMixin, TimeUpdateMixin


if TYPE_CHECKING:
    from .order import Order


class Client(TimeCreateMixin, TimeUpdateMixin, Base):

    uuid_id: so.Mapped[uuid.UUID] = so.mapped_column(
        PgUUID(as_uuid=True),
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )

    phone: so.Mapped[str] = so.mapped_column(sa.String(255), unique=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)

    first_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), nullable=True)
    last_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), nullable=True)

    orders: so.Mapped[list["Order"]] = so.relationship(
        "Order", back_populates="client",
        cascade="all, delete-orphan",
    )
