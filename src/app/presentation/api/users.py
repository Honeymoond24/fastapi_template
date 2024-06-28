from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.application.users import CreateUserInteractor
from .schemas import UserCreate, SomeResult

users_router = APIRouter(route_class=DishkaRoute)


@users_router.post("/alternative")
async def add_users_alternative(
        user_create: UserCreate,
        # new_user: Annotated[CreateUserInteractor, Depends(Stub(CreateUserInteractor))],
        new_user: FromDishka[CreateUserInteractor],
) -> SomeResult:
    user_id = await new_user(user_create.username)
    return SomeResult(
        user_id=user_id,
    )
