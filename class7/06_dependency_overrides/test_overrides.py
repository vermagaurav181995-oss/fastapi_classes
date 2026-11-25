import pytest

from emails import get_email_sender
from main import app
from security import get_current_user

FAKE_ADMIN = {"id": 100, "email": "boss@example.com", "role": "admin"}
FAKE_USER = {"id": 200, "email": "ana@example.com", "role": "user"}


def fake_admin() -> dict:
    return FAKE_ADMIN


def fake_user() -> dict:
    return FAKE_USER


@pytest.fixture
def as_admin():
    app.dependency_overrides[get_current_user] = fake_admin
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def as_user():
    app.dependency_overrides[get_current_user] = fake_user
    yield
    app.dependency_overrides.clear()


class FakeEmailSender:

    def __init__(self):
        self.sent: list[tuple[str, str]] = []

    def send(self, to: str, subject: str) -> None:
        self.sent.append((to, subject))


@pytest.fixture
def fake_sender():
    sender = FakeEmailSender()
    app.dependency_overrides[get_email_sender] = lambda: sender
    yield sender
    app.dependency_overrides.clear()


def test_me_as_fake_user_needs_no_token(client, as_user):
    response = client.get("/auth/me")
    assert response.status_code == 200
    assert response.json() == FAKE_USER


def test_override_flows_through_require_role_as_admin(client, as_admin):
    assert client.delete("/books/1").status_code == 204


def test_override_flows_through_require_role_as_user(client, as_user):
    assert client.delete("/books/1").status_code == 403


def test_create_book_as_fake_user(client, as_user):
    assert client.post("/books", json={"title": "Emma", "price": 5}).status_code == 201


def test_without_override_the_real_check_is_back(client):
    assert app.dependency_overrides == {}
    assert client.delete("/books/1").status_code == 401


def test_register_uses_the_fake_email_sender(client, fake_sender):
    response = client.post("/auth/register", json={"email": "ana@example.com", "password": "anapass123"})
    assert response.status_code == 201
    assert fake_sender.sent == [("ana@example.com", "Welcome to the bookstore!")]


def test_failed_register_sends_no_email(client, fake_sender):
    client.post("/auth/register", json={"email": "ana@example.com", "password": "anapass123"})
    client.post("/auth/register", json={"email": "ana@example.com", "password": "anapass123"})
    assert len(fake_sender.sent) == 1


def test_real_sender_is_used_without_override(client):
    from storage import SENT_EMAILS

    client.post("/auth/register", json={"email": "ben@example.com", "password": "benpass123"})
    assert SENT_EMAILS == [{"to": "ben@example.com", "subject": "Welcome to the bookstore!"}]
