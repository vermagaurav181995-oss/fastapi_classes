import pytest

from main import app
from security import get_current_user


@pytest.fixture
def as_admin():
    app.dependency_overrides[get_current_user] = lambda: {"id": 99, "email": "boss@example.com", "role": "admin"}
    yield
    app.dependency_overrides.clear()


def test_admin_override_allows_delete(client, as_admin):
    assert client.delete("/books/1").status_code == 204


def test_override_is_gone_afterwards(client):
    assert app.dependency_overrides == {}
    assert client.delete("/books/1").status_code == 401
