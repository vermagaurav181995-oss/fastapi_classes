ANA = {"email": "ana@example.com", "password": "anapass123"}


def auth_headers(client, email: str, password: str) -> dict:
    response = client.post("/auth/login", data={"username": email, "password": password})
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_register_returns_201(client):
    response = client.post("/auth/register", json=ANA)
    assert response.status_code == 201
    assert "password" not in response.text


def test_duplicate_email_returns_409(client):
    client.post("/auth/register", json=ANA)
    assert client.post("/auth/register", json=ANA).status_code == 409


def test_wrong_password_returns_401(client):
    client.post("/auth/register", json=ANA)
    response = client.post("/auth/login", data={"username": ANA["email"], "password": "nope"})
    assert response.status_code == 401


def test_auth_headers_helper_works(client):
    client.post("/auth/register", json=ANA)
    assert client.get("/auth/me", headers=auth_headers(client, **ANA)).json()["email"] == ANA["email"]
