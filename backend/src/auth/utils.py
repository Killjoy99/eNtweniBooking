from datetime import datetime, timedelta
from typing import Any

import jwt

from src.core import config



def create_access_token(subject: str | Any, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, config.JWT_ACCESS_SECRET_KEY, config.ENCRYPTION_ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: str | Any, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, config.JWT_REFRESH_SECRET_KEY, config.ENCRYPTION_ALGORITHM)
    return encoded_jwt
