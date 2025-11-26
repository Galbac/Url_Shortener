from typing import Any, AsyncGenerator

from dishka import Provider, provide, Scope, make_async_container
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)

from src.core.config import settings


class DatabaseProvider(Provider):

    @provide(scope=Scope.APP)
    def create_engine(self) -> AsyncEngine:
        return create_async_engine(settings.async_database_url)

    @provide(scope=Scope.APP)
    def create_session(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_factory: async_sessionmaker[AsyncSession]) -> AsyncGenerator[Any, Any]:
        async with session_factory() as session:
            yield session


container = make_async_container(
    DatabaseProvider(),
)