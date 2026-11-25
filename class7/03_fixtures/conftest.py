import pytest
from fastapi.testclient import TestClient

from main import BOOKS, app, seed_books


@pytest.fixture(autouse=True)
def reset_books():
    BOOKS.clear()
    seed_books()
    yield
    BOOKS.clear()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
