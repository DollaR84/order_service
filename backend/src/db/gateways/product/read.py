from typing import Optional

from sqlalchemy import select
from sqlalchemy.sql import Select

from db import domain

from ..base import BaseGateway

from ...models import Product


class GetProductGateway(BaseGateway[int, Product]):

    async def get_product(self, product_id: int) -> Optional[domain.ProductModel]:
        error_message = f"Error get product id={product_id}"

        stmt = select(Product)
        stmt = stmt.where(Product.id == product_id)

        product = await self._get(stmt, error_message)
        return domain.ProductModel(**product.to_dict()) if product else None

    async def get_products(
            self,
            name: Optional[str] = None,
            description: Optional[str] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[domain.ProductModel]:
        error_message = "Error get products"
        stmt = select(Product)

        stmt = self._build_conditions(stmt, name, description)
        stmt = stmt.order_by(Product.id)

        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        products = await self._get(stmt, error_message, is_multiple=True)
        return [
            domain.ProductModel(**product.to_dict())
            for product in products
        ]

    def _build_conditions(
            self,
            stmt: Select,
            name: Optional[str] = None,
            description: Optional[str] = None,
    ) -> Select:
        if name:
            stmt = stmt.where(Product.name.icontains(name))

        if description:
            stmt = stmt.where(Product.description.icontains(description))

        return stmt
