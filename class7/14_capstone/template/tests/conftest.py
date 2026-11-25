import os

os.environ["SECRET_KEY"] = "test-secret-key-that-is-at-least-32-characters-long"
os.environ["ENVIRONMENT"] = "development"
os.environ["ADMIN_EMAIL"] = "admin@example.com"
os.environ["ADMIN_PASSWORD"] = "admin12345"

import pytest
from fastapi.testclient import TestClient

from main import app
from storage import ITEMS, USERS


@pytest.fixture(autouse=True)
def reset_data():
    for table in (USERS, ITEMS):
        table.clear()
    yield
    for table in (USERS, ITEMS):
        table.clear()
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def auth_headers(client: TestClient, email: str, password: str) -> dict:
    response = client.post("/auth/login", data={"username": email, "password": password})
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def register_and_login(client: TestClient, email: str, password: str = "password123") -> dict:
    assert client.post("/auth/register", json={"email": email, "password": password}).status_code == 201
    return auth_headers(client, email, password)


@pytest.fixture
def admin_headers(client) -> dict:
    return auth_headers(client, "admin@example.com", "admin12345")


@pytest.fixture
def ana_headers(client) -> dict:
    return register_and_login(client, "ana@example.com")


@pytest.fixture
def ben_headers(client) -> dict:
    return register_and_login(client, "ben@example.com")
