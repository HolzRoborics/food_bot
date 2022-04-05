from pydantic import BaseSettings


class ToolConfig:
    env_file_encoding = "utf-8"
    extra = "ignore"


class BotSettings(BaseSettings):
    TOKEN: str
    ITEMS_PER_PAGE: int = 8

    class Config(ToolConfig):
        env_prefix = "bot_"


class PostgresSettings(BaseSettings):
    URI: str
    ALEMBIC_URI: str
    MAX_OVERFLOW: int = 15
    POOL_SIZE: int = 15

    class Config(ToolConfig):
        env_prefix = "postgres_"


class RedisSettings(BaseSettings):
    URI: str

    class Config(ToolConfig):
        env_prefix = "redis_"


bot_settings = BotSettings()
postgres_settings = PostgresSettings()
redis_settings = RedisSettings()
