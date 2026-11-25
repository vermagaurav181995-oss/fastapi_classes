from conftest import auth_headers
from security import create_access_token


def test_register_returns_201_without_password(client):
    response = client.post("/auth/register", json={"email": "ana@example.com", "password": "password123"})
    assert response.status_code == 201
    assert response.json() == {"id": 2, "email": "ana@example.com", "role": "user"}
    assert "password" not in response.text


def test_register_duplicate_email_returns_409(client, ana_headers):
    response = client.post("/auth/register", json={"email": "ana@example.com", "password": "password123"})
    assert response.status_code == 409


def test_register_short_password_returns_422(client):
    assert client.post("/auth/register", json={"email": "x@example.com", "password": "short"}).status_code == 422


def test_login_wrong_password_returns_401(client, ana_headers):
    response = client.post("/auth/login", data={"username": "ana@example.com", "password": "wrong"})
    assert response.status_code == 401


def test_me_returns_current_user(client, ana_headers):
    assert client.get("/auth/me", headers=ana_headers).json()["email"] == "ana@example.com"


def test_me_without_token_returns_401(client):
    assert client.get("/auth/me").status_code == 401


def test_me_with_fake_token_returns_401(client):
    assert client.get("/auth/me", headers={"Authorization": "Bearer fake"}).status_code == 401


def test_me_with_expired_token_returns_401(client, ana_headers):
    expired = create_access_token(user_id=2, expires_minutes=-1)
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {expired}"}).status_code == 401


def test_admin_is_seeded(client):
    me = client.get("/auth/me", headers=auth_headers(client, "admin@example.com", "admin12345"))
    assert me.json()["role"] == "admin"
