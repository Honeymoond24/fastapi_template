from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.protocols.database import DatabaseGateway, UoW
from app.application.users import new_user, NewUser
from .depends_stub import Stub
from .schemas import UserCreate, SomeResult, UserID

users_router = APIRouter()


@users_router.post("")
async def add_users(
        user_create: UserCreate,
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> UserID:
    user_id = await new_user(database, uow, user_create.username)
    return UserID(
        id=user_id,
    )


@users_router.post("/alternative")
async def add_users_alternative(
        user_create: UserCreate,
        new_user: Annotated[NewUser, Depends(Stub(NewUser))],
) -> SomeResult:
    user_id = await new_user(user_create.username)
    return SomeResult(
        user_id=user_id,
    )
