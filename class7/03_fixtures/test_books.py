def test_starts_with_three_books(client):
    assert len(client.get("/books").json()) == 3


def test_add_a_book(client):
    response = client.post("/books", json={"title": "Emma", "price": 5})
    assert response.status_code == 201
    assert response.json()["id"] == 4
    assert len(client.get("/books").json()) == 4


def test_still_three_books_after_adding_one(client):
    assert len(client.get("/books").json()) == 3


def test_new_book_always_gets_id_4(client):
    assert client.post("/books", json={"title": "Persuasion", "price": 6}).json()["id"] == 4


def test_deleted_data_comes_back(client):
    from main import BOOKS

    BOOKS.clear()
    assert client.get("/books").json() == []


def test_data_is_back_after_breaking_it(client):
    assert [book["title"] for book in client.get("/books").json()] == ["Dune", "1984", "Neuromancer"]
