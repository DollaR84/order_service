from typing import Optional

from application import dto
from application import interfaces


class BaseGetProduct:

    def __init__(self, gateway: interfaces.GetProductInterface):
        self.gateway = gateway


class GetProduct(BaseGetProduct):

    async def __call__(self, product_id: int) -> Optional[dto.Product]:
        domain_data = await self.gateway.get_product(product_id)
        return dto.Product(**domain_data.dict()) if domain_data else None


class GetProducts(BaseGetProduct):

    async def __call__(
            self,
            name: Optional[str] = None,
            description: Optional[str] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[dto.Product]:
        domain_data = await self.gateway.get_products(name, description, offset, limit)
        return [
            dto.Product(**product.dict())
            for product in domain_data
        ]
