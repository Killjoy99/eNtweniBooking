import logging
import os
import base64
from urllib import parse
from typing import List
from pydantic import BaseModel

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

log = logging.getLogger(__name__)


class BaseConfigurationModel(BaseModel):
    """Base configuration model used by all config options."""

    pass


def get_env_tags(tag_list: List[str]) -> dict:
    """Create dictionary of available env tags."""
    tags = {}
    for t in tag_list:
        tag_key, env_key = t.split(":")

        env_value = os.environ.get(env_key)

        if env_value:
            tags.update({tag_key: env_value})

    return tags


config = Config(".env")

SECRET_PROVIDER = config("SECRET_PROVIDER", default=None)
if SECRET_PROVIDER == "metatron-secret":
    import metatron.decrypt

    class Secret:
        """
        Holds a string value that should not be revealed in tracebacks etc.
        You should cast the value to `str` at the point it is required.
        """

        def __init__(self, value: str):
            self._value = value
            self._decrypted_value = (
                metatron.decrypt.MetatronDecryptor()
                .decryptBytes(base64.b64decode(self._value))
                .decode("utf-8")
            )

        def __repr__(self) -> str:
            class_name = self.__class__.__name__
            return f"{class_name}('**********')"

        def __str__(self) -> str:
            return self._decrypted_value

elif SECRET_PROVIDER == "kms-secret":
    import boto3

    class Secret:
        """
        Holds a string value that should not be revealed in tracebacks etc.
        You should cast the value to `str` at the point it is required.
        """

        def __init__(self, value: str):
            self._value = value
            self._decrypted_value = (
                boto3.client("kms")
                .decrypt(CiphertextBlob=base64.b64decode(value))["Plaintext"]
                .decode("utf-8")
            )

        def __repr__(self) -> str:
            class_name = self.__class__.__name__
            return f"{class_name}('**********')"

        def __str__(self) -> str:
            return self._decrypted_value

else:
    from starlette.datastructures import Secret


LOG_LEVEL = config("LOG_LEVEL", default=logging.WARNING)
ENV = config("ENV", default="local")

ENV_TAG_LIST = config("ENV_TAGS", cast=CommaSeparatedStrings, default="")
ENV_TAGS = get_env_tags(ENV_TAG_LIST)

ENTWENIBOOKING_UI_URL = config("ENTWENIBOOKING_UI_URL", default="http://localhost:8080")

# static files
DEFAULT_STATIC_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), os.path.join("static")
)
STATIC_DIR = config("STATIC_DIR", default=DEFAULT_STATIC_DIR)

# # database
# DATABASE_HOSTNAME = config("DATABASE_HOSTNAME")
# DATABASE_CREDENTIALS = config("DATABASE_CREDENTIALS", cast=Secret)
# # this will support special chars for credentials
# _DATABASE_CREDENTIAL_USER, _DATABASE_CREDENTIAL_PASSWORD = str(DATABASE_CREDENTIALS).split(":")
# _QUOTED_DATABASE_PASSWORD = parse.quote(str(_DATABASE_CREDENTIAL_PASSWORD))
# DATABASE_NAME = config("DATABASE_NAME", default="dispatch")
# DATABASE_PORT = config("DATABASE_PORT", default="5432")
# DATABASE_ENGINE_POOL_SIZE = config("DATABASE_ENGINE_POOL_SIZE", cast=int, default=20)
# DATABASE_ENGINE_MAX_OVERFLOW = config("DATABASE_ENGINE_MAX_OVERFLOW", cast=int, default=0)
# # Deal with DB disconnects
# # https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-disconnects
# DATABASE_ENGINE_POOL_PING = config("DATABASE_ENGINE_POOL_PING", default=False)
# SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{_DATABASE_CREDENTIAL_USER}:{_QUOTED_DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"
