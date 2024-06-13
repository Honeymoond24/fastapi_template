from functools import partial
from logging import getLogger
from typing import AsyncGenerator, Any

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
from sqlalchemy.orm import Session

from app.adapters.sqlalchemy_db.gateway import SqlaGateway
from app.adapters.sqlalchemy_db.models import start_mappers
from app.api.depends_stub import Stub
from app.application.models import User
from app.application.protocols.database import DatabaseGateway, UoW
from app.application.users import NewUser
from app.config import settings

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


def new_gateway(session: Session = Depends(Stub(Session))):
    yield SqlaGateway(session)


def new_uow(session: Session = Depends(Stub(Session))):
    return session


def create_async_session_maker() -> async_sessionmaker[AsyncSession]:
    engine: AsyncEngine = create_async_engine(
        str(settings.DB_URI),
        echo=True,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "timeout": 5,
        },
    )
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def new_session(session_maker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, Any]:
    async with session_maker() as session:
        yield session


def init_dependencies(app: FastAPI):
    # start_mappers()

    async_session_maker = create_async_session_maker()

    app.dependency_overrides[Session] = partial(new_session, async_session_maker)
    app.dependency_overrides[DatabaseGateway] = new_gateway
    app.dependency_overrides[UoW] = new_uow

    app.dependency_overrides[NewUser] = NewUser
    all_depends(NewUser)
