import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt
from fastapi import HTTPException, Response, status
from passlib.context import CryptContext

from .config import auth_settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_access_token(
    login_identifier: str | Any,
    expires_delta: int = None,
    user_data: dict = {},
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + timedelta(expires_delta)  # type: ignore
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(
            minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "sub": str(login_identifier),
        "exp": expires_delta,
        "user_data": user_data,
    }
    encoded_jwt = jwt.encode(
        to_encode,
        auth_settings.JWT_ACCESS_SECRET_KEY,
        auth_settings.ENCRYPTION_ALGORITHM,
    )
    return encoded_jwt


async def decode_access_token(token: str) -> dict:
    """Decodes a JWT and returns its payload"""
    try:
        payload = jwt.decode(
            token,
            auth_settings.JWT_ACCESS_SECRET_KEY,
            [auth_settings.ENCRYPTION_ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


async def create_refresh_token(
    login_identifier: str | Any, expires_delta: float = 0.0, user_data: dict = {}
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)  # type: ignore
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(
            minutes=auth_settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "sub": str(login_identifier),
        "exp": expires_delta,
        "user_data": user_data,
    }
    encoded_jwt = jwt.encode(
        to_encode,
        auth_settings.JWT_REFRESH_SECRET_KEY,
        auth_settings.ENCRYPTION_ALGORITHM,
    )
    return encoded_jwt


async def decode_refresh_token(token: str) -> dict:
    """Decodes a JWT and returns its payload"""
    try:
        payload = jwt.decode(
            token,
            auth_settings.JWT_REFRESH_SECRET_KEY,
            [auth_settings.ENCRYPTION_ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


async def generate_password_hash(password: str) -> str:
    return password_context.hash(password)


async def verify_password_hash(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


async def generate_secure_password(length=20) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(alphabet) for _ in range(length))

    return password


async def set_cookies_and_json(
    response: Response, access_token: str, refresh_token: str
) -> Dict[str, str]:
    """Set HTTP-only cookies and include them in the JSON response."""
    cookies = {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="none",
        secure=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="none",
        secure=True,
    )

    return cookies
