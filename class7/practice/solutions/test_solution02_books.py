import pytest


def test_existing_book_returns_200(client):
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Dune", "price": 9.99}


def test_missing_book_returns_404(client):
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}


@pytest.mark.parametrize("bad_id", [0, -1, "abc"])
def test_invalid_id_returns_422(client, bad_id):
    assert client.get(f"/books/{bad_id}").status_code == 422
