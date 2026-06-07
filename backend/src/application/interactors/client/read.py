from typing import Optional
import uuid

from application import dto
from application import interfaces


class BaseGetClient:

    def __init__(self, gateway: interfaces.GetClientInterface):
        self.gateway = gateway


class GetClientByID(BaseGetClient):

    async def __call__(self, client_id: int) -> Optional[dto.Client]:
        domain_data = await self.gateway.get_client_by_id(client_id)
        return dto.Client(**domain_data.dict()) if domain_data else None


class GetClientByUUID(BaseGetClient):

    async def __call__(self, uuid_id: uuid.UUID) -> Optional[dto.Client]:
        domain_data = await self.gateway.get_client_by_uuid(uuid_id)
        return dto.Client(**domain_data.dict()) if domain_data else None


class GetClientByPhone(BaseGetClient):

    async def __call__(self, phone: str) -> Optional[dto.Client]:
        domain_data = await self.gateway.get_client_by_phone(phone)
        return dto.Client(**domain_data.dict()) if domain_data else None


class GetClients(BaseGetClient):

    async def __call__(
            self,
            data: dto.ClientSearchFilters,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[dto.Client]:
        domain_data = await self.gateway.get_clients(
            data.phone,
            data.email,
            data.first_name,
            data.last_name,
            offset,
            limit
        )
        return [
            dto.Client(**client.dict())
            for client in domain_data
        ]
