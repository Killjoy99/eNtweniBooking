import secrets
import asyncio
import string
import passlib
import jwt

from datetime import datetime, timedelta
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, func

# from src.core.config import settings
from .models import User
from .schemas import UserCreateSchema, UserLoginSchema, UserReadSchema


# Authenticate a user based on username/email and password
async def authenticate_user(db_session: AsyncSession, login_identifier: str, password: str) -> User | None:
    # introduce a small delay to mitigate user enumeration attacks
    await asyncio.sleep(0.1)
    
    user: User | None = await get_user_by_login_identifier(db_session, login_identifier=login_identifier)
    
    if not user:
        return None
    
    # if the user has been found, check password
    if not verify_password(plain_password=password, hashed_password=user.password):
        return None
    
    return user

# Get a user with either email or username provided
async def get_user_by_login_identifier(db_session: AsyncSession, *, login_identifier: str) -> User | None:
    query = select(User).where(or_(User.email == login_identifier, User.username == login_identifier))
    result = await db_session.execute(query)
    user: User = result.scalar_one_or_none()
    
    return user
