from typing import Optional
import uuid

from sqlalchemy import select
from sqlalchemy.sql import Select

from db import domain

from ..base import BaseGateway

from ...models import Client


class GetClientGateway(BaseGateway[int, Client]):

    async def get_client_by_id(self, client_id: int) -> Optional[domain.ClientModel]:
        error_message = f"Error get client by id='{client_id}'"
        stmt = select(Client)
        stmt = stmt.where(Client.id == client_id)
        return await self._get_client(stmt, error_message)

    async def get_client_by_uuid(self, uuid_id: uuid.UUID) -> Optional[domain.ClientModel]:
        error_message = f"Error get client by uuid='{uuid_id}'"
        stmt = select(Client)
        stmt = stmt.where(Client.uuid_id == uuid_id)
        return await self._get_client(stmt, error_message)

    async def get_client_by_phone(self, phone: str) -> Optional[domain.ClientModel]:
        error_message = f"Error get client by phone='{phone}'"
        stmt = select(Client)
        stmt = stmt.where(Client.phone == phone)
        return await self._get_client(stmt, error_message)

    async def get_clients(
            self,
            phone: Optional[str] = None,
            email: Optional[str] = None,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[domain.ClientModel]:
        error_message = "Error get clients"
        stmt = select(Client)

        stmt = self._build_conditions(stmt, phone, email, first_name, last_name)
        stmt = stmt.order_by(Client.id)

        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        clients = await self._get(stmt, error_message, is_multiple=True)
        return [
            domain.ClientModel(**client.to_dict())
            for client in clients
        ]

    def _build_conditions(
            self,
            stmt: Select,
            phone: Optional[str] = None,
            email: Optional[str] = None,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
    ) -> Select:
        if phone:
            stmt = stmt.where(Client.phone.icontains(phone))

        if email:
            stmt = stmt.where(Client.email.icontains(email))

        if first_name:
            stmt = stmt.where(Client.first_name.icontains(first_name))

        if last_name:
            stmt = stmt.where(Client.last_name.icontains(last_name))

        return stmt

    async def _get_client(self, stmt: Select, error_message: str) -> Optional[domain.ClientModel]:
        client = await self._get(stmt, error_message)
        if client:
            return domain.ClientModel(**client.to_dict())
        return None
