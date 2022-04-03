from pydantic import BaseSettings


class ToolConfig:
    env_file_encoding = "utf-8"
    extra = "ignore"


class ProjectSettings(BaseSettings):
    class Config(ToolConfig):
        env_prefix = "project_"


class PostgresSettings(BaseSettings):
    URI: str
    ALEMBIC_URI: str
    MAX_OVERFLOW: int = 15
    POOL_SIZE: int = 15

    class Config(ToolConfig):
        env_prefix = "postgres_"


project_settings = ProjectSettings()
postgres_settings = PostgresSettings()
