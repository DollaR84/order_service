from typing import Optional

from application import dto
from application import interfaces


class BaseGetOrder:

    def __init__(self, gateway: interfaces.GetOrderInterface):
        self.gateway = gateway


class GetOrder(BaseGetOrder):

    async def __call__(self, order_id: int) -> Optional[dto.Order]:
        domain_data = await self.gateway.get_order(order_id)
        return dto.Order(
            id=domain_data.id,
            client_id=domain_data.client_id,
            total_price=domain_data.total_price,
            status=domain_data.status,
            created_at=domain_data.created_at,
            updated_at=domain_data.updated_at,
            items=[dto.OrderItem(**item.dict()) for item in domain_data.items],
        ) if domain_data else None


class GetOrders(BaseGetOrder):

    async def __call__(self, client_id: Optional[int] = None) -> list[dto.Order]:
        domain_data = await self.gateway.get_orders(client_id)
        return [
            dto.Order(
                id=order.id,
                client_id=order.client_id,
                total_price=order.total_price,
                status=order.status,
                created_at=order.created_at,
                updated_at=order.updated_at,
                items=[dto.OrderItem(**item.dict()) for item in order.items],
            ) for order in domain_data
        ]
