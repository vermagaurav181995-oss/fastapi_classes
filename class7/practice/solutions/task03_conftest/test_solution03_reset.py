from storage import BOOKS


def test_add_a_book(client):
    BOOKS[4] = {"id": 4, "title": "Emma", "price": 5}
    assert len(client.get("/books").json()) == 4


def test_still_three_books(client):
    assert len(client.get("/books").json()) == 3
