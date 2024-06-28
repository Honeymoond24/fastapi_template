from abc import abstractmethod
from typing import Protocol

from app.application.models import User


class UoW(Protocol):
    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def flush(self):
        raise NotImplementedError


class DatabaseGateway(Protocol):
    @abstractmethod
    def add_user(self, user: User) -> None:
        raise NotImplementedError
