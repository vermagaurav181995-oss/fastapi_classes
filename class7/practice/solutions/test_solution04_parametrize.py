import pytest

INVALID_PAYLOADS = [
    pytest.param({"title": "", "price": 5}, id="empty-title"),
    pytest.param({"title": "x" * 201, "price": 5}, id="title-too-long"),
    pytest.param({"title": "Emma", "price": 0}, id="price-zero"),
    pytest.param({"title": "Emma", "price": -5}, id="price-negative"),
    pytest.param({"title": "Emma"}, id="missing-price"),
    pytest.param({"price": 5}, id="missing-title"),
]


@pytest.fixture
def token_headers(client) -> dict:
    client.post("/auth/register", json={"email": "ana@example.com", "password": "anapass123"})
    token = client.post("/auth/login", data={"username": "ana@example.com", "password": "anapass123"}).json()
    return {"Authorization": f"Bearer {token['access_token']}"}


@pytest.mark.parametrize("payload", INVALID_PAYLOADS)
def test_invalid_book_returns_422(client, token_headers, payload):
    assert client.post("/books", json=payload, headers=token_headers).status_code == 422
