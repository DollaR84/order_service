from abc import abstractmethod
from typing import Optional, Protocol

from db import domain


class GetOrderInterface(Protocol):

    @abstractmethod
    async def get_order(self, order_id: int) -> Optional[domain.OrderModel]:
        ...

    async def get_orders(self, client_id: Optional[int] = None) -> list[domain.OrderModel]:
        ...
