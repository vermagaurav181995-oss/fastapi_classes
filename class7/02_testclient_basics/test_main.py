from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_book_returns_200():
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Dune", "price": 9.99}


def test_get_missing_book_returns_404():
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}


def test_book_id_zero_returns_422():
    response = client.get("/books/0")
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["path", "book_id"]


def test_create_book_returns_201():
    response = client.post("/books", json={"title": "Emma", "price": 5.5})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Emma" and data["price"] == 5.5
    assert client.get(f"/books/{data['id']}").status_code == 200


def test_send_json_body():
    response = client.post("/books", json={"title": "", "price": 5})
    assert response.status_code == 422


def test_send_query_params():
    response = client.get("/search", params={"q": "du"})
    assert response.status_code == 200
    assert [book["title"] for book in response.json()["results"]] == ["Dune"]


def test_send_headers():
    response = client.get("/client", headers={"X-Client": "pytest"})
    assert response.json() == {"client": "pytest"}
    assert client.get("/client").status_code == 422


def test_send_form_data():
    response = client.post("/login", data={"username": "ana", "password": "secret"})
    assert response.status_code == 200
    assert client.post("/login", data={"username": "ana", "password": "wrong"}).status_code == 401


def test_upload_a_file():
    response = client.post("/upload", files={"file": ("notes.txt", b"hello world", "text/plain")})
    assert response.json() == {"filename": "notes.txt", "size": 11}


def test_send_cookies():
    assert client.get("/session").status_code == 401
    client.cookies.set("session_id", "abc123")
    assert client.get("/session").json() == {"session_id": "abc123"}
    client.cookies.clear()
