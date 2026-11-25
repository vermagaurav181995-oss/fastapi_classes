import os

os.environ["SECRET_KEY"] = "test-secret-key-that-is-at-least-32-characters-long"
os.environ["ADMIN_EMAIL"] = "admin@example.com"
os.environ["ADMIN_PASSWORD"] = "admin12345"

import pytest
from fastapi.testclient import TestClient

from main import app
from storage import BOOKS, SENT_EMAILS, USERS, seed_books


@pytest.fixture(autouse=True)
def reset_data():
    BOOKS.clear()
    USERS.clear()
    SENT_EMAILS.clear()
    seed_books()
    yield
    BOOKS.clear()
    USERS.clear()
    SENT_EMAILS.clear()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def auth_headers(client: TestClient, email: str, password: str) -> dict:
    response = client.post("/auth/login", data={"username": email, "password": password})
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture
def admin_headers(client) -> dict:
    return auth_headers(client, "admin@example.com", "admin12345")


@pytest.fixture
def user_headers(client) -> dict:
    client.post("/auth/register", json={"email": "ana@example.com", "password": "anapass123"})
    return auth_headers(client, "ana@example.com", "anapass123")
