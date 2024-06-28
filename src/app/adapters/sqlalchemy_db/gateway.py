from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.adapters.sqlalchemy_db.models import start_mappers
from app.application.models import User
from app.application.protocols.database import DatabaseGateway


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    def add_user(self, user: User) -> None:
        self.session.add(user)
        return


start_mappers()
