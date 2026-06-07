from application import dto
from application import interfaces

from db import domain


class CreateOrder:

    def __init__(self, gateway: interfaces.CreateOrderInterface):
        self.gateway = gateway

    async def __call__(self, data: dto.NewOrder) -> int:
        domain_data = domain.NewOrderModel(
            client_id=data.client_id,
            status=data.status,
            items=[
                domain.NewOrderItemModel(**item.dict())
                for item in data.items
            ]
        )

        return await self.gateway.create_order(domain_data)
