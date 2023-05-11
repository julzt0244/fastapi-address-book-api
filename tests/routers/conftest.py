import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from address_book.database import (
    Base,
    DatabaseEnv,
    create_db_engine_and_session,
    get_db,
)
from address_book.main import app


@pytest.fixture(scope="module")
def test_engine_and_db() -> tuple[Engine, sessionmaker]:
    engine, TestingSessionLocal = create_db_engine_and_session(DatabaseEnv.Test)
    Base.metadata.create_all(bind=engine)

    return engine, TestingSessionLocal


@pytest.fixture(scope="module")
def test_client(test_engine_and_db: tuple[Engine, sessionmaker]):
    engine, TestingSessionLocal = test_engine_and_db
    Base.metadata.create_all(bind=engine)

    client = TestClient(app)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    return client


@pytest.fixture(scope="module")
def get_authed_user_1_headers(
    test_engine_and_db: tuple[Engine, sessionmaker], test_client: TestClient
):
    # region Setup
    engine, _ = test_engine_and_db

    Base.metadata.create_all(bind=engine)

    test_username = "testuser1"
    test_password = "testpassword"

    _ = test_client.post(
        "/account/",
        json={"username": test_username, "password": test_password},
    )
    response = test_client.post(
        "/account/session/",
        data={"username": test_username, "password": test_password},
    )
    assert response.status_code == 200
    data = response.json()

    # endregion

    header: dict[str, str] = {"Authorization": "Bearer " + data["access_token"]}
    yield header

    # region Teardown

    Base.metadata.drop_all(bind=engine)

    # endregion


@pytest.fixture(scope="module")
def get_authed_user_2_headers(
    test_engine_and_db: tuple[Engine, sessionmaker], test_client: TestClient
):
    # region Setup
    engine, _ = test_engine_and_db

    Base.metadata.create_all(bind=engine)

    test_username = "testuser2"
    test_password = "testpassword"

    _ = test_client.post(
        "/account/",
        json={"username": test_username, "password": test_password},
    )
    response = test_client.post(
        "/account/session/",
        data={"username": test_username, "password": test_password},
    )
    assert response.status_code == 200
    data = response.json()

    # endregion

    header: dict[str, str] = {"Authorization": "Bearer " + data["access_token"]}
    yield header

    # region Teardown

    Base.metadata.drop_all(bind=engine)

    # endregion
