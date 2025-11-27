from typing import Any, AsyncGenerator

from dishka import Provider, provide, Scope, make_async_container
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)

from src.core.config import settings
from src.repositories.url_repo import URLRepository
from src.services.url_service import URLService


class DatabaseProvider(Provider):

    @provide(scope=Scope.APP)
    def create_engine(self) -> AsyncEngine:
        return create_async_engine(settings.async_database_url)

    @provide(scope=Scope.APP)
    def create_session(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_factory: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, Any]:
        async with session_factory() as session:
            yield session


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def repo(self, session: AsyncSession) -> URLRepository:
        return URLRepository(session)


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_url_service(self, repo: URLRepository) -> URLService:
        return URLService(repo)


container = make_async_container(
    DatabaseProvider(),
    RepositoryProvider(),
    ServiceProvider()
)
