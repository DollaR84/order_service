from abc import abstractmethod
from typing import Protocol

from db import domain


class CreateProductInterface(Protocol):

    @abstractmethod
    async def create_product(self, data: domain.NewProductModel) -> int:
        ...
