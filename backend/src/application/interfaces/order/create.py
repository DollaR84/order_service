from abc import abstractmethod
from typing import Protocol

from db import domain


class CreateOrderInterface(Protocol):

    @abstractmethod
    async def create_order(self, data: domain.NewOrderModel) -> int:
        ...
