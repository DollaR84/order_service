from abc import abstractmethod
from typing import Protocol

from db import domain


class CreateClientInterface(Protocol):

    @abstractmethod
    async def create_client(self, data: domain.NewClientModel) -> int:
        ...
