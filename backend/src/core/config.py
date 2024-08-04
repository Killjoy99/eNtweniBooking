import logging
import os
from os import path
from random import randint

import boto3
from pydantic_settings import BaseSettings, SettingsConfigDict


class GlobalSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ENVIRONMENT: str = "development"
    # App Settings
    ALLOWED_ORIGINS: str = "http://127.0.0.1:3000,http://localhost:3000"

    #################################### logging ####################################
    LOG_LEVEL: int = logging.DEBUG
    #################################### logging ####################################

    #################################### sentry ####################################
    SENTRY_DSN: str = ""
    #################################### sentry ####################################

    #################################### static files ####################################
    STATIC_HOST: str = "http://localhost:8001"
    DEFAULT_STATIC_DIR: str = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), os.path.join("../static")
    )
    STATIC_DIR: str = DEFAULT_STATIC_DIR
    TEMPLATE_DIR: str = path.join(STATIC_DIR, "templates")
    #################################### static files ####################################


class TestSettings(GlobalSettings):
    DATABASE_SCHEMA: str = f"test_{randint(1, 100)}"


class DevelopmentSettings(GlobalSettings):
    pass


class ProductionSettings(GlobalSettings):
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION_NAME: str = ""
    AWS_IMAGES_BUCKET: str = ""

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

            return s3_resource.meta.client  # type: ignore
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
