import logging
import os
import base64
from urllib import parse
from typing import List
from pydantic import BaseModel

from starlette.config import Config

config = Config(".env")


class BaseConfigurationModel(BaseModel):
    """Base configuration model used by all config options."""
    pass


ENTWENIBOOKING_UI_URL = config("ENTWENIBOOKING_UI_URL", default="http://localhost:8080")


# auth
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
ENCRYPTION_ALGORITHM = config("ENCRYPTION_ALGORITHM", default="HS256")
JWT_ACCESS_SECRET_KEY = config("JWT_ACCESS_SECRET_KEY", cast=int, default=86400)  # Seconds

JWT_REFRESH_SECRET_KEY = config("JWT_REFRESH_SECRET_KEY", default=None)
REFRESH_TOKEN_EXPIRE_MINUTES = config("REFRESH_TOKEN_EXPIRE_MINUTES", cast=int, default=86400)  # Seconds

# static files
DEFAULT_STATIC_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.join("../static"))
STATIC_DIR = config("STATIC_DIR", default=DEFAULT_STATIC_DIR)

# database
DATABASE_HOSTNAME = config("DATABASE_HOSTNAME")
DATABASE_CREDENTIALS = config("DATABASE_CREDENTIALS")
# this will support special chars for credentials
_DATABASE_CREDENTIAL_USER, _DATABASE_CREDENTIAL_PASSWORD = str(DATABASE_CREDENTIALS).split(":")
_QUOTED_DATABASE_PASSWORD = parse.quote(str(_DATABASE_CREDENTIAL_PASSWORD))
DATABASE_NAME = config("DATABASE_NAME", default="entwenibooking")
DATABASE_PORT = config("DATABASE_PORT", default="5432")
DATABASE_ENGINE_POOL_SIZE = config("DATABASE_ENGINE_POOL_SIZE", cast=int, default=20)
DATABASE_ENGINE_MAX_OVERFLOW = config("DATABASE_ENGINE_MAX_OVERFLOW", cast=int, default=0)
# Deal with DB disconnects
# https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-disconnects
DATABASE_ENGINE_POOL_PING = config("DATABASE_ENGINE_POOL_PING", default=False)
SQLALCHEMY_DATABASE_URI = f"postgresql+asyncpg://{_DATABASE_CREDENTIAL_USER}:{_QUOTED_DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"
