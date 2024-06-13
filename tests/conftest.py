# pylint: disable=redefined-outer-name
import asyncio
from typing import Generator, AsyncGenerator

import async_timeout
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, AsyncConnection, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.adapters.sqlalchemy_db.models import metadata_obj
from app.config import settings
from app.main import create_app


async def wait_for_postgres_to_come_up(engine: AsyncEngine) -> AsyncConnection:
    async with async_timeout.timeout(10):
        return engine.connect()


@pytest.fixture(scope="session")
def postgres_async_engine() -> AsyncEngine:
    engine: AsyncEngine = create_async_engine(
        str(settings.DB_URI)
    )
    yield engine
    engine.sync_engine.dispose()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def postgres_create(postgres_async_engine: AsyncEngine) -> AsyncGenerator:
    await wait_for_postgres_to_come_up(postgres_async_engine)
    async with postgres_async_engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)
    yield
    # async with postgres_async_engine.begin() as conn:
    #     await conn.run_sync(metadata_obj.drop_all)


@pytest_asyncio.fixture
async def postgres_session_factory(
        postgres_async_engine: AsyncEngine,
        postgres_create: AsyncGenerator
) -> Generator[async_sessionmaker, None, None]:
    yield async_sessionmaker(
        bind=postgres_async_engine, expire_on_commit=False, class_=AsyncSession
    )


@pytest_asyncio.fixture
async def postgres_session(postgres_session_factory: async_sessionmaker):
    return await postgres_session_factory()


@pytest.fixture(scope="session")
async def client():
    # noinspection PyTypeChecker
    # TODO: should check this place with MyPy
    async with AsyncClient(transport=ASGITransport(app=create_app()), base_url="http://test") as async_client:
        yield async_client
