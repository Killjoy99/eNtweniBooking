import logging
import os
import asyncio
from os import path
from random import randint
from urllib import parse

import boto3
from pydantic_settings import BaseSettings, SettingsConfigDict

class GlobalSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="data/.env", env_file_encoding="utf-8")
    
    ENVIRONMENT: str = "development"
    # App Settings
    ALLOWED_ORIGINS: str = "http://127.0.0.1:3000,http://localhost:3000"
    
    #################################### logging ####################################
    LOG_LEVEL: int = logging.DEBUG
    #################################### logging ####################################
    
    #################################### sentry ####################################
    SENTRY_DSN: str = ""
    #################################### sentry ####################################
    
    #################################### Database ####################################
    DATABASE_USER: str = "serpent99"
    DATABASE_PASSWORD: str = "Mamlangeni0711"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: str = "5432"
    DATABASE_NAME: str = "entwenibooking"
    DATABASE_SCHEMA: str = "entwenibooking"
    DATABASE_ENGINE_POOL_SIZE: int = 20
    DATABASE_ENGINE_MAX_OVERFLOW: int = 0
    # Deal with DB disconnects
    # https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-disconnects
    DATABASE_ENGINE_POOL_PING: bool = False
    # this will support special chars for credentials
    _QUOTED_DATABASE_PASSWORD: str = parse.quote(str(DATABASE_PASSWORD))
    # specify a single database URL
    DATABASE_URL: str = f"postgresql+asyncpg://{DATABASE_USER}:{_QUOTED_DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    #################################### Database ####################################
    
    #################################### static files ####################################
    STATIC_HOST: str = "http://localhost:8001"
    DEFAULT_STATIC_DIR: str = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.join("../static"))
    STATIC_DIR: str = DEFAULT_STATIC_DIR
    TEMPLATE_DIR: str = path.join(STATIC_DIR, "templates")
    #################################### static files ####################################

    
    #################################### auth related ####################################
    JWT_ACCESS_SECRET_KEY: str = "9d9bc4d77ac3a6fce1869ec8222729d2"
    JWT_REFRESH_SECRET_KEY: str = "fdc5635260b464a0b8e12835800c9016"
    ENCRYPTION_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    NEW_ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    # Google Auth
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_USERINFO_URL: str = "https://www.googleapis.com/oauth2/v3/userinfo"
    GOOGLE_AUTH_URL: str = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_TOKEN_URL: str = "https://oauth2.googleapis.com/token"
    REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/callback"
    #################################### auth related ####################################
    
    #################################### admin ####################################
    ADMIN_SECRET_KEY: str = "Hv9LGqARc473ceBUYDw1FR0QaXOA3Ky4"
    #################################### admin ####################################

    #################################### redis for caching ####################################
    REDIS_CACHE_ENABLED: bool = True
    REDIS_HOST: str = "chat-redis"
    REDIS_PORT: str | int = 6379
    REDIS_PASSWORD: str | None = None
    REDIS_CACHE_EXPIRATION_SECONDS: int = 60 * 30
    REDIS_DB: int = 0
    #################################### redis for caching ####################################
    
    
class TestSettings(GlobalSettings):
    DATABASE_SCHEMA: str = f"test_{randint(1, 100)}"
    
    
class DevelopmentSettings(GlobalSettings):
    pass


class ProductionSettings(GlobalSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION_NAME: str
    AWS_IMAGES_BUCKET: str

    LOG_LEVEL: int = logging.INFO
    
    @staticmethod
    def get_aws_client_for_image_upload():
        if all(
            (
                aws_access_key_id := os.environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key := os.environ.get("AWS_SECRET_ACCESS_KEY"),
                region_name := os.environ.get("AWS_REGION_NAME", ""),
            )
        ):
            aws_session = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name,
            )
            s3_resource = aws_session.resource("s3")

            return s3_resource.meta.client
        else:
            return None
        

def get_settings():
    env = os.environ.get("ENVIRONMENT", "development")
    if env == "test":
        return TestSettings()
    elif env == "development":
        return DevelopmentSettings()
    elif env == "production":
        return ProductionSettings()
    
    return GlobalSettings()


settings = get_settings()


LOGGING_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": settings.LOG_LEVEL,
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "": {"handlers": ["default"], "level": settings.LOG_LEVEL, "propagate": False},
        "uvicorn": {
            "handlers": ["default"],
            "level": logging.ERROR,
            "propagate": False,
        },
    },
}
