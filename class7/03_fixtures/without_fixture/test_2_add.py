from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_add_a_book():
    response = client.post("/books", json={"title": "Emma", "price": 5})
    assert response.status_code == 201
    assert response.json()["id"] == 4
