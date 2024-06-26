from .models import User
from .protocols.database import DatabaseGateway, UoW


async def new_user(
        database: DatabaseGateway,
        uow: UoW,
        name: str,
) -> int:
    user = User(name=name)
    database.add_user(user)
    await uow.commit()
    return user.id


# alternative implementation using classes
class CreateUserInteractor:
    def __init__(
            self,
            database: DatabaseGateway,
            uow: UoW,
    ):
        self.database = database
        self.uow = uow

    async def __call__(
            self, name: str,
    ) -> int:
        user = User(name=name)
        self.database.add_user(user)
        await self.uow.commit()
        return user.id
