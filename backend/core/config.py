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
ENTWENIBOOKING_JWT_SECRET = config("ENTWENIBOOKING_JWT_SECRET", default=None)
ENTWENIBOOKING_JWT_ALG = config("ENTWENIBOOKING_JWT_ALG", default="HS256")
ENTWENIBOOKING_JWT_EXP = config("ENTWENIBOOKING_JWT_EXP", cast=int, default=86400)  # Seconds

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
