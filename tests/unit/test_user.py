from typing import Coroutine
from unittest.mock import Mock, AsyncMock

import pytest
import pytest_asyncio
from dishka import Provider, Scope, provide, make_async_container, AsyncContainer

from app.application.protocols.database import DatabaseGateway, UoW
from app.application.users import CreateUserInteractor
from app.main.di import interactor_provider


class AdaptersProvider(Provider):
    scope = Scope.APP

    @provide
    def database_gateway(self) -> DatabaseGateway:
        gateway = Mock()
        gateway.add_user = Mock(return_value=None)
        return gateway

    @provide
    def unit_of_work(self) -> UoW:
        uow = Mock()
        uow.commit = AsyncMock()
        return uow


@pytest_asyncio.fixture
async def container():
    providers = [AdaptersProvider(), interactor_provider()]
    c: AsyncContainer = make_async_container(*providers)
    async with c() as request_container:
        yield request_container


async def test_user_create(container):
    user_create = await container.get(CreateUserInteractor)
    print(f"{type(user_create)=}")
    print(f"{type(user_create.database)=}")
    print(f"{type(user_create.uow)=}")
    user_id = await user_create("test_user1")
    (await container.get(UoW)).commit.assert_awaited()
