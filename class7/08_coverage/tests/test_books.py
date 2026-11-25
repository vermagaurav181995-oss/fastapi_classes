import pytest


def test_root(client):
    assert client.get("/").status_code == 200


def test_list_books(client):
    assert [book["title"] for book in client.get("/books").json()] == ["Dune", "1984", "Neuromancer"]


def test_list_books_pagination(client):
    assert [book["id"] for book in client.get("/books?skip=1&limit=1").json()] == [2]


def test_get_book(client):
    assert client.get("/books/1").json() == {"id": 1, "title": "Dune", "price": 9.99}


@pytest.mark.parametrize(("book_id", "status"), [(0, 422), (999, 404), ("abc", 422)])
def test_get_book_errors(client, book_id, status):
    assert client.get(f"/books/{book_id}").status_code == status


def test_create_book_as_user(client, user_headers):
    response = client.post("/books", json={"title": "Emma", "price": 5}, headers=user_headers)
    assert response.status_code == 201
    assert response.json() == {"id": 4, "title": "Emma", "price": 5.0}


def test_create_book_without_token_returns_401(client):
    assert client.post("/books", json={"title": "Emma", "price": 5}).status_code == 401


@pytest.mark.parametrize("payload", [{"title": "", "price": 5}, {"title": "Emma", "price": 0}, {"title": "Emma"}])
def test_create_invalid_book_returns_422(client, user_headers, payload):
    assert client.post("/books", json=payload, headers=user_headers).status_code == 422


def test_delete_without_token_returns_401(client):
    assert client.delete("/books/1").status_code == 401


def test_delete_as_user_returns_403(client, user_headers):
    assert client.delete("/books/1", headers=user_headers).status_code == 403


def test_delete_as_admin_returns_204(client, admin_headers):
    assert client.delete("/books/1", headers=admin_headers).status_code == 204
    assert client.get("/books/1").status_code == 404


def test_delete_missing_book_returns_404(client, admin_headers):
    assert client.delete("/books/999", headers=admin_headers).status_code == 404
