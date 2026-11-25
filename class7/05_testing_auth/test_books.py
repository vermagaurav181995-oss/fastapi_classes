def test_delete_without_token_returns_401(client):
    assert client.delete("/books/1").status_code == 401


def test_delete_as_normal_user_returns_403(client, user_headers):
    response = client.delete("/books/1", headers=user_headers)
    assert response.status_code == 403
    assert response.json() == {"detail": "Not enough permissions"}
    assert client.get("/books/1").status_code == 200


def test_delete_as_admin_returns_204(client, admin_headers):
    response = client.delete("/books/1", headers=admin_headers)
    assert response.status_code == 204
    assert response.content == b""
    assert client.get("/books/1").status_code == 404


def test_delete_missing_book_as_admin_returns_404(client, admin_headers):
    assert client.delete("/books/999", headers=admin_headers).status_code == 404


def test_logged_in_user_can_add_a_book(client, user_headers):
    response = client.post("/books", json={"title": "Emma", "price": 5}, headers=user_headers)
    assert response.status_code == 201
    assert client.post("/books", json={"title": "Emma", "price": 5}).status_code == 401
