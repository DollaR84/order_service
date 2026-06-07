from typing import AsyncGenerator

from dishka import from_context, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from application import interfaces

from core.config import Config

from db import PostgresDbConnector
from db.base import BaseDbConnector
from db import gateways


class DBProvider(Provider):

    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_db(self, config: Config) -> BaseDbConnector:
        return PostgresDbConnector(
            config.db.uri,
            config.db.debug,
            config.db.ssl
        )

    @provide(scope=Scope.APP)
    async def get_db_engine(self, db: BaseDbConnector) -> AsyncEngine:
        return db.engine

    @provide(scope=Scope.REQUEST)
    async def db_session(self, connector: BaseDbConnector) -> AsyncGenerator[AsyncSession, None]:
        async with connector.get_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    @provide(scope=Scope.REQUEST)
    async def client_creator(self, session: AsyncSession) -> interfaces.CreateClientInterface:
        return gateways.CreateClientGateway(session)

    @provide(scope=Scope.REQUEST)
    async def client_getter(self, session: AsyncSession) -> interfaces.GetClientInterface:
        return gateways.GetClientGateway(session)

    @provide(scope=Scope.REQUEST)
    async def order_creator(self, session: AsyncSession) -> interfaces.CreateOrderInterface:
        return gateways.CreateOrderGateway(session)

    @provide(scope=Scope.REQUEST)
    async def order_getter(self, session: AsyncSession) -> interfaces.GetOrderInterface:
        return gateways.GetOrderGateway(session)

    @provide(scope=Scope.REQUEST)
    async def product_creator(self, session: AsyncSession) -> interfaces.CreateProductInterface:
        return gateways.CreateProductGateway(session)

    @provide(scope=Scope.REQUEST)
    async def product_getter(self, session: AsyncSession) -> interfaces.GetProductInterface:
        return gateways.GetProductGateway(session)
