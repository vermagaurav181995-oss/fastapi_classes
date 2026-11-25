from conftest import auth_headers
from security import create_access_token
from storage import SENT_EMAILS, USERS

ANA = {"email": "ana@example.com", "password": "anapass123"}


def test_register_returns_201_without_password(client):
    response = client.post("/auth/register", json=ANA)
    assert response.status_code == 201
    assert response.json() == {"id": 2, "email": "ana@example.com", "role": "user"}
    assert "password" not in response.text


def test_register_sends_welcome_email(client):
    client.post("/auth/register", json=ANA)
    assert SENT_EMAILS == [{"to": "ana@example.com", "subject": "Welcome to the bookstore!"}]


def test_register_duplicate_returns_409(client):
    client.post("/auth/register", json=ANA)
    assert client.post("/auth/register", json=ANA).status_code == 409


def test_register_invalid_payload_returns_422(client):
    assert client.post("/auth/register", json={"email": "not-an-email", "password": "x"}).status_code == 422


def test_login_and_me(client):
    client.post("/auth/register", json=ANA)
    response = client.get("/auth/me", headers=auth_headers(client, ANA["email"], ANA["password"]))
    assert response.status_code == 200
    assert response.json()["email"] == ANA["email"]


def test_login_wrong_password_returns_401(client):
    client.post("/auth/register", json=ANA)
    response = client.post("/auth/login", data={"username": ANA["email"], "password": "nope"})
    assert response.status_code == 401


def test_me_without_token_returns_401(client):
    assert client.get("/auth/me").status_code == 401


def test_me_with_fake_token_returns_401(client):
    assert client.get("/auth/me", headers={"Authorization": "Bearer fake"}).status_code == 401


def test_me_with_expired_token_returns_401(client, user_headers):
    expired = create_access_token(user_id=2, expires_minutes=-1)
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {expired}"}).status_code == 401


def test_me_after_user_was_deleted_returns_401(client, user_headers):
    USERS.pop(2)
    assert client.get("/auth/me", headers=user_headers).status_code == 401


def test_admin_is_seeded_once(client):
    from main import seed_admin

    seed_admin()
    admins = [user for user in USERS.values() if user["role"] == "admin"]
    assert len(admins) == 1
