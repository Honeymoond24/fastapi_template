from sqlalchemy import Integer, String, Column, MetaData, Table
from sqlalchemy.orm import registry, declarative_base

from app.application.models import User

Base = declarative_base()
metadata_obj = MetaData()
mapper_registry = registry()

user = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String()),
)


# class User(Base):
#     __tablename__ = "user"


mapper_registry.map_imperatively(User, user)
