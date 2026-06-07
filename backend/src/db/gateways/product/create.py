from sqlalchemy import insert

from db import domain

from ..base import BaseGateway

from ...models import Product


class CreateProductGateway(BaseGateway[int, Product]):

    async def create_product(self, data: domain.NewProductModel) -> int:
        stmt = insert(Product).values(**data.dict(exclude_unset=True)).returning(Product.id)
        error_message = "Error creating new product"

        return await self._create(stmt, error_message)
