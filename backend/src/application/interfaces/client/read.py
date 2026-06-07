from abc import abstractmethod
from typing import Optional, Protocol
import uuid

from db import domain


class GetClientInterface(Protocol):

    @abstractmethod
    async def get_client_by_id(self, client_id: int) -> Optional[domain.ClientModel]:
        ...

    @abstractmethod
    async def get_client_by_uuid(self, uuid_id: uuid.UUID) -> Optional[domain.ClientModel]:
        ...

    @abstractmethod
    async def get_client_by_phone(self, phone: str) -> Optional[domain.ClientModel]:
        ...

    async def get_clients(
            self,
            phone: Optional[str] = None,
            email: Optional[str] = None,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[domain.ClientModel]:
        ...
