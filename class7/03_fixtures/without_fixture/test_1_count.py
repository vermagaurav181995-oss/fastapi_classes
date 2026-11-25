from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_there_are_three_books():
    assert len(client.get("/books").json()) == 3
