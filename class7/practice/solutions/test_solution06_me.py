from security import create_access_token


def test_me_without_token(client):
    response = client.get("/auth/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_me_with_fake_token(client):
    response = client.get("/auth/me", headers={"Authorization": "Bearer fake.token.value"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_me_with_real_token(client):
    client.post("/auth/register", json={"email": "ana@example.com", "password": "anapass123"})
    token = client.post("/auth/login", data={"username": "ana@example.com", "password": "anapass123"}).json()
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token['access_token']}"})
    assert response.status_code == 200
    assert response.json()["email"] == "ana@example.com"


def test_me_with_expired_token(client):
    expired = create_access_token(user_id=1, expires_minutes=-1)
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {expired}"}).status_code == 401
