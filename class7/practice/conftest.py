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
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
