import pytest
from fastapi.testclient import TestClient

from main import app
from storage import BOOKS, USERS, seed_books


@pytest.fixture(autouse=True)
def reset_data():
    BOOKS.clear()
    USERS.clear()
    seed_books()
    yield
    BOOKS.clear()
    USERS.clear()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
