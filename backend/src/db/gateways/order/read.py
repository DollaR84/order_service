from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db import domain
from ..base import BaseGateway
from ...models import Order


class GetOrderGateway(BaseGateway[int, Order]):

    async def get_order(self, order_id: int) -> Optional[domain.OrderModel]:
        error_message = f"Error getting order #{order_id}"

        stmt = select(Order)
        stmt = stmt.where(Order.id == order_id)
        stmt = stmt.options(selectinload(Order.items))

        order = await self._get(stmt, error_message)
        return self._to_domain(order) if order else None

    async def get_orders(self, client_id: Optional[int] = None) -> list[domain.OrderModel]:
        error_message = "Error getting orders"

        stmt = select(Order)
        if client_id:
            stmt = stmt.where(Order.client_id == client_id)
        stmt = stmt.options(selectinload(Order.items))
        stmt = stmt.order_by(Order.id.desc())

        orders = await self._get(stmt, error_message, is_multiple=True)

        return [
            self._to_domain(order)
            for order in orders
        ]

    def _to_domain(self, order: Order) -> domain.OrderModel:
        return domain.OrderModel(
            id=order.id,
            client_id=order.client_id,
            status=order.status,
            total_price=order.total_price,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=[
                domain.OrderItemModel(**item.to_dict())
                for item in order.items
            ]
        )
