from application import dto
from application import interfaces

from db import domain


class CreateProduct:

    def __init__(self, gateway: interfaces.CreateProductInterface):
        self.gateway = gateway

    async def __call__(self, data: dto.NewProduct) -> int:
        domain_data = domain.NewProductModel(**data.dict())
        return await self.gateway.create_product(domain_data)
