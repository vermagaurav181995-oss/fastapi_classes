def login(client, email: str, password: str) -> dict:
    token = client.post("/auth/login", data={"username": email, "password": password}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_delete_without_token_is_401(client):
    assert client.delete("/books/1").status_code == 401


def test_delete_as_normal_user_is_403(client):
    client.post("/auth/register", json={"email": "ana@example.com", "password": "anapass123"})
    assert client.delete("/books/1", headers=login(client, "ana@example.com", "anapass123")).status_code == 403


def test_delete_as_admin_is_204(client):
    assert client.delete("/books/1", headers=login(client, "admin@example.com", "admin12345")).status_code == 204
    assert client.get("/books/1").status_code == 404
