from application import dto
from application import interfaces

from db import domain


class CreateClient:

    def __init__(self, gateway: interfaces.CreateClientInterface):
        self.gateway = gateway

    async def __call__(self, data: dto.NewClient) -> int:
        domain_data = domain.NewClientModel(**data.dict())
        return await self.gateway.create_client(domain_data)
