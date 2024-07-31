from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib import parse


class DatabaseSettings(BaseSettings):
    
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
    
    #################################### redis for caching ####################################
    REDIS_CACHE_ENABLED: bool = True
    REDIS_HOST: str = "chat-redis"
    REDIS_PORT: str | int = 6379
    REDIS_PASSWORD: str | None = None
    REDIS_CACHE_EXPIRATION_SECONDS: int = 60 * 30
    REDIS_DB: int = 0
    #################################### redis for caching ####################################
    
database_settings = DatabaseSettings()
# configure for different screnarios(dev, test, prod)
