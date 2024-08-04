from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import Boolean, DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .config import database_settings

DATABASE_URL = database_settings.DATABASE_URL or (
    f"postgresql+asyncpg://{database_settings.DATABASE_USER}:{database_settings.DATABASE_PASSWORD}@{database_settings.DATABASE_HOST}:{database_settings.DATABASE_PORT}/{database_settings.DATABASE_NAME}"
)

async_engine = create_async_engine(
    database_settings.DATABASE_URL,
    pool_size=database_settings.DATABASE_ENGINE_POOL_SIZE,
    max_overflow=database_settings.DATABASE_ENGINE_MAX_OVERFLOW,
    pool_pre_ping=database_settings.DATABASE_ENGINE_POOL_PING,
    isolation_level="AUTOCOMMIT",
)
AsyncSessionLocal = async_sessionmaker(bind=async_engine)


class RemoveBaseFieldMixin:
    created_at: None
    updated_at: None
    is_deleted: None


class Base(DeclarativeBase):
    __abstract__ = True
    # TODO: find a way to not create a schema each time a table is created

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_engine.begin() as async_conn:
        await async_conn.run_sync(Base.metadata.create_all)

    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
