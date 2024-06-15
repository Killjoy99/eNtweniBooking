import re
import functools
from typing import Any, Annotated

from fastapi import Depends
from fastapi.requests import Request
from pydantic import BaseModel


from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# from sqlalchemy import create_engine, inspect
# from sqlalchemy.sql.expression import true
# from sqlalchemy.orm import object_session, sessionmaker, Session, declarative_base, declared_attr

from core import config

async_engine = create_async_engine(
    config.SQLALCHEMY_DATABASE_URI,
    pool_size=config.DATABASE_ENGINE_POOL_SIZE,
    max_overflow=config.DATABASE_ENGINE_MAX_OVERFLOW,
    pool_pre_ping=config.DATABASE_ENGINE_POOL_PING,
)
AsyncSessionLocal = async_sessionmaker(bind=async_engine)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_engine.begin() as async_conn:
        await async_conn.run_sync(Base.metadata.create_all)
        
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()