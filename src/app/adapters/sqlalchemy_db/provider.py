from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine, AsyncEngine

from app.config import settings


def create_async_session_maker() -> async_sessionmaker[AsyncSession]:
    engine: AsyncEngine = create_async_engine(
        str(settings.DB_URI),
        echo=True,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "timeout": 5,
        },
    )
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)
