import jwt
import secrets
import string

from fastapi import Depends, Cookie, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import Any, Annotated

from passlib.context import CryptContext

from src.core.config import settings
from src.database.core import get_async_db

from .models import User, UserRoles


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_access_token(login_identifier: str | Any, expires_delta: int = None, user_data: dict = {}) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode = {
        "sub": str(login_identifier),
        "exp": expires_delta,
        "user_data": user_data
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_ACCESS_SECRET_KEY, settings.ENCRYPTION_ALGORITHM)
    return encoded_jwt

async def decode_access_token(token: str) -> dict:
    """Decodes a JWT and returns its payload"""
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, settings.ENCRYPTION_ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def create_refresh_token(login_identifier: str | Any, expires_delta: int = None, user_data: dict = {}) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(login_identifier),
        "exp": expires_delta,
        "user_data": user_data
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ENCRYPTION_ALGORITHM)
    return encoded_jwt

async def decode_refresh_token(token: str) -> dict:
    """Decodes a JWT and returns its payload"""
    try:
        payload = jwt.decode(token, settings.JWT_REFRESH_SECRET_KEY, settings.ENCRYPTION_ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")



async def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


async def generate_secure_password(length=20) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(alphabet) for _ in range(length))
    
    return password
