from typing import Iterable

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlmodel import SQLModel, Session
from testcontainers.postgres import PostgresContainer

from app.db_config import DatabaseConfig, get_database_config


@pytest.fixture(scope="session", autouse=True)
def test_database_config(request: pytest.FixtureRequest) -> DatabaseConfig:
    postgres = PostgresContainer("postgres:15-alpine")
    postgres.start()

    def remove_containers() -> None:
        postgres.stop()

    request.addfinalizer(remove_containers)

    database_config = DatabaseConfig(
        host=postgres.get_container_host_ip(),
        port=postgres.get_exposed_port(5432),
        username=postgres.username,
        password=postgres.password,
        database=postgres.dbname,
    )

    from app.db_config import get_database_engine

    SQLModel.metadata.create_all(get_database_engine(database_config))

    return database_config


@pytest.fixture(scope="session")
def test_database_engine(test_database_config: DatabaseConfig) -> Engine:
    from app.db_config import get_database_engine
    return get_database_engine(test_database_config)


@pytest.fixture(scope="session")
def test_database_session(test_database_engine: Engine) -> Iterable[Session]:
    from app.db_config import get_database_session
    yield from get_database_session(test_database_engine)


@pytest.fixture
def test_client(test_database_config: DatabaseConfig) -> TestClient:
    import app.main as web

    web.app.dependency_overrides[get_database_config] = lambda: test_database_config

    return TestClient(web.app)


pytest_plugins = [
    "tests.fixtures.book",
    "tests.fixtures.customer",
    "tests.fixtures.employee",
    "tests.fixtures.order",
]
