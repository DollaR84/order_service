from abc import abstractmethod
from typing import Optional, Protocol

from db import domain


class GetProductInterface(Protocol):

    @abstractmethod
    async def get_product(self, product_id: int) -> Optional[domain.ProductModel]:
        ...

    async def get_products(
            self,
            name: Optional[str] = None,
            description: Optional[str] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[domain.ProductModel]:
        ...
