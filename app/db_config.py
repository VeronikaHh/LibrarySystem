from collections.abc import Iterator
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from sqlalchemy import Engine
from sqlmodel import (
    Session,
    create_engine,
)

from .config import (
    ROOT_DIR,
    SERVICE_NAME,
)

DEFAULT_DB_DIALECT = "postgresql"


class DatabaseConfig(BaseSettings):
    # host: str
    # port: int
    # username: str
    # password: str
    # database: str
    # dialect: str = DEFAULT_DB_DIALECT
    database_url: str

    model_config = SettingsConfigDict(
        env_prefix=SERVICE_NAME + "DB_",
        env_file=ROOT_DIR / Path(".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_database_config() -> DatabaseConfig:
    return DatabaseConfig()


def get_connection_string(database_config: Annotated[DatabaseConfig, Depends(get_database_config)]) -> str:
    # return (
    #     f"{database_config.dialect}://"
    #     f"{database_config.username}:{database_config.password}@"
    #     f"{database_config.host}:{database_config.port}/"
    #     f"{database_config.database}"
    # )
    return database_config.database_url


def get_database_engine(database_config: Annotated[DatabaseConfig, Depends(get_database_config)]) -> Engine:
    return create_engine(get_connection_string(database_config))


def get_database_session(engine: Annotated[Engine, Depends(get_database_engine)]) -> Iterator[Session]:
    with Session(engine) as session:
        yield session
