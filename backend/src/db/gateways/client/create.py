from sqlalchemy import insert

from db import domain

from ..base import BaseGateway

from ...models import Client


class CreateClientGateway(BaseGateway[int, Client]):

    async def create_client(self, data: domain.NewClientModel) -> int:
        stmt = insert(Client).values(**data.dict()).returning(Client.id)
        error_message = "Error creating new client"

        return await self._create(stmt, error_message)
