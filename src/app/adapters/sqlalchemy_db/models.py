from sqlalchemy import Integer, String, MetaData, Table, Column
from sqlalchemy.orm import registry

from app.application.models import User

# created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
# updated_at = Annotated[datetime.datetime, mapped_column(
#     server_default=text("TIMEZONE('utc', now())"),
#     onupdate=text("TIMEZONE('utc', now())"),
# )]

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata_obj = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)
mapper_registry = registry()

user = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String()),
)


def start_mappers():
    mapper_registry.map_imperatively(User, user)


start_mappers()
