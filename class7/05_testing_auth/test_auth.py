from conftest import auth_headers
from security import create_access_token

ANA = {"email": "ana@example.com", "password": "anapass123"}


def test_register_then_me(client):
    response = client.post("/auth/register", json=ANA)
    assert response.status_code == 201
    assert response.json() == {"id": 2, "email": "ana@example.com", "role": "user"}

    me = client.get("/auth/me", headers=auth_headers(client, ANA["email"], ANA["password"]))
    assert me.status_code == 200
    assert me.json()["email"] == "ana@example.com"


def test_password_hash_never_in_response(client):
    response = client.post("/auth/register", json=ANA)
    body = response.text
    assert "password" not in body
    assert "hashed_password" not in body
    assert "$argon2" not in body


def test_duplicate_email_returns_409(client):
    assert client.post("/auth/register", json=ANA).status_code == 201
    response = client.post("/auth/register", json=ANA)
    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}


def test_short_password_returns_422(client):
    assert client.post("/auth/register", json={**ANA, "password": "short"}).status_code == 422


def test_wrong_password_returns_401(client):
    client.post("/auth/register", json=ANA)
    response = client.post("/auth/login", data={"username": ANA["email"], "password": "wrong-password"})
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_unknown_email_gets_the_same_401(client):
    wrong_email = client.post("/auth/login", data={"username": "nobody@example.com", "password": "x"})
    client.post("/auth/register", json=ANA)
    wrong_password = client.post("/auth/login", data={"username": ANA["email"], "password": "x"})
    assert wrong_email.status_code == wrong_password.status_code == 401
    assert wrong_email.json() == wrong_password.json()


def test_me_without_token_returns_401(client):
    response = client.get("/auth/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_me_with_fake_token_returns_401(client):
    response = client.get("/auth/me", headers={"Authorization": "Bearer this.is.fake"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_me_with_expired_token_returns_401(client, user_headers):
    expired_token = create_access_token(user_id=2, expires_minutes=-1)
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401
