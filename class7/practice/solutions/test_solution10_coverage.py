from security import create_access_token
from storage import USERS


def headers_for(client, email, password):
    token = client.post("/auth/login", data={"username": email, "password": password}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_root_and_list_pagination(client):
    assert client.get("/").status_code == 200
    assert [b["id"] for b in client.get("/books?skip=1&limit=1").json()] == [2]


def test_create_book_and_missing_delete(client):
    admin = headers_for(client, "admin@example.com", "admin12345")
    assert client.post("/books", json={"title": "Emma", "price": 5}, headers=admin).status_code == 201
    assert client.delete("/books/999", headers=admin).status_code == 404


def test_token_for_deleted_user(client):
    token = create_access_token(user_id=1)
    USERS.clear()
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_welcome_email_is_sent(client):
    from storage import SENT_EMAILS

    client.post("/auth/register", json={"email": "ana@example.com", "password": "anapass123"})
    assert SENT_EMAILS == [{"to": "ana@example.com", "subject": "Welcome to the bookstore!"}]
