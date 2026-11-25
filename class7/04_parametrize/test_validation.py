import pytest

INVALID_PAYLOADS = [
    pytest.param({"title": "", "price": 10}, id="empty-title"),
    pytest.param({"title": "x" * 201, "price": 10}, id="title-201-chars"),
    pytest.param({"title": "Emma", "price": 0}, id="price-zero"),
    pytest.param({"title": "Emma", "price": -5}, id="price-negative"),
    pytest.param({"title": "Emma"}, id="missing-price"),
    pytest.param({"price": 10}, id="missing-title"),
]


@pytest.mark.parametrize("payload", INVALID_PAYLOADS)
def test_invalid_book_returns_422(client, payload):
    response = client.post("/books", json=payload)
    assert response.status_code == 422


@pytest.mark.parametrize(
    ("book_id", "expected_title"),
    [(1, "Dune"), (2, "1984"), (3, "Neuromancer")],
)
def test_valid_ids_return_the_right_book(client, book_id, expected_title):
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == expected_title


@pytest.mark.parametrize(
    ("book_id", "expected_status"),
    [(0, 422), (-1, 422), (999, 404), ("abc", 422)],
)
def test_bad_ids(client, book_id, expected_status):
    assert client.get(f"/books/{book_id}").status_code == expected_status


def test_boundary_values_are_accepted(client):
    assert client.post("/books", json={"title": "x", "price": 0.01}).status_code == 201
    assert client.post("/books", json={"title": "x" * 200, "price": 1}).status_code == 201
