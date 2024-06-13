from app.api.depends_stub import Stub
from app.application.users import NewUser


async def test_user_create():
    user_create = NewUser(database=Stub(), uow=Stub())
    user_id = await user_create("user")
    assert user_id == 1
