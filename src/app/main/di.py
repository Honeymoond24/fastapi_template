from logging import getLogger
from typing import AsyncIterable

from dishka import make_async_container, Provider, Scope, provide, AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.adapters.sqlalchemy_db.gateway import SqlaGateway
from app.adapters.sqlalchemy_db.provider import create_async_session_maker
from app.application.protocols.database import DatabaseGateway, UoW
from app.application.users import CreateUserInteractor
from app.presentation.api.depends_stub import Stub

logger = getLogger(__name__)


def all_depends(cls: type) -> None:
    """
    Adds `Depends()` to the class `__init__` methods, so it can be used
    a fastapi dependency having own dependencies
    """
    init = cls.__init__  # type: ignore
    total_ars = init.__code__.co_kwonlyargcount + init.__code__.co_argcount - 1
    init.__defaults__ = tuple(
        Depends() for _ in range(total_ars)
    )


def new_gateway(async_session: AsyncSession = Depends(Stub(AsyncSession))):
    yield SqlaGateway(async_session)


def new_uow(async_session: AsyncSession = Depends(Stub(AsyncSession))):
    return async_session


async def new_async_session(async_session_maker: async_sessionmaker[AsyncSession]) -> AsyncSession:
    async with async_session_maker() as async_session:
        yield async_session


# def db_provider() -> Provider:
#     provider = Provider()
#
#     provider.provide(get_engine, scope=Scope.APP)
#     provider.provide(get_async_sessionmaker, scope=Scope.APP)
#     provider.provide(get_async_session, scope=Scope.REQUEST)
#
#     return provider


class DBProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_async_session_maker(self) -> async_sessionmaker[AsyncSession]:
        return create_async_session_maker()

    @provide(scope=Scope.REQUEST)
    async def get_async_session(
            self,
            async_session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with async_session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_database_gateway(self, async_session: AsyncSession) -> DatabaseGateway:
        return SqlaGateway(async_session)

    @provide(scope=Scope.REQUEST)
    def get_uow(self, async_session: AsyncSession) -> UoW:
        return async_session


def interactor_provider() -> Provider:
    provider = Provider()

    provider.provide(CreateUserInteractor, scope=Scope.REQUEST)
    # provider.provide(DeleteUserInteractor, scope=Scope.REQUEST)
    # provider.provide(GetUserInteractor, scope=Scope.REQUEST)
    # provider.provide(AuthorizeInteractor, scope=Scope.REQUEST)

    return provider


def setup_interactors() -> list[Provider]:
    providers = [
        DBProvider(),
        interactor_provider(),
    ]
    return providers


def init_dependencies(app: FastAPI):
    providers: list[Provider] = setup_interactors()
    container: AsyncContainer = make_async_container(*providers)
    setup_dishka(container, app)
