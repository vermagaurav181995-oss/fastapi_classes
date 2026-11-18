import importlib
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

HERE = Path(__file__).parent
BUGS = HERE / "04_spot_the_bug"
TEST_SECRET = "revision-test-secret-" + "x" * 43
TEST_API_KEY = "revision-test-api-key"
PNG_BYTES = b"\x89PNG\r\n\x1a\n" + b"\x00" * 32

os.environ.update(
    SECRET_KEY=TEST_SECRET,
    API_KEY=TEST_API_KEY,
    ADMIN_EMAIL="admin@example.com",
    ADMIN_PASSWORD="admin12345",
)


def load_app(folder: Path) -> tuple[object, dict]:
    before = set(sys.modules)
    sys.path.insert(0, str(folder))
    try:
        importlib.import_module("main")
    finally:
        sys.path.remove(str(folder))
    loaded = {}
    for name in set(sys.modules) - before:
        if (getattr(sys.modules[name], "__file__", None) or "").startswith(str(folder)):
            loaded[name] = sys.modules.pop(name)
    return loaded["main"], loaded


@pytest.fixture
def open_app():
    clients = []

    def _open(folder: Path) -> tuple[TestClient, dict]:
        main, modules = load_app(folder)
        client = TestClient(main.app)
        client.__enter__()
        clients.append(client)
        return client, modules

    yield _open
    for client in clients:
        client.__exit__(None, None, None)


def login_headers(client: TestClient, email: str, password: str) -> dict:
    response = client.post("/auth/login", data={"username": email, "password": password})
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def register(client: TestClient, email: str, password: str):
    return client.post("/auth/register", json={"email": email, "password": password})


def test_01_request_journey(open_app, capsys):
    client, modules = open_app(HERE / "01_request_journey")
    admin = login_headers(client, "admin@example.com", "admin12345")
    user = login_headers(client, "user@example.com", "user12345")

    assert client.delete("/books/1").status_code == 401
    response = client.delete("/books/0", headers=admin)
    assert response.status_code == 422 and response.json()["detail"][0]["loc"] == ["path", "book_id"]
    response = client.delete("/books/1", headers=user)
    assert response.status_code == 403 and response.json()["detail"] == "Not enough permissions"
    response = client.delete("/books/99", headers=admin)
    assert response.status_code == 404
    assert response.json() == {"error": "BookNotFound", "message": "Book 99 does not exist"}

    capsys.readouterr()
    response = client.delete("/books/1", headers=admin)
    assert response.status_code == 204 and response.content == b""
    assert "X-Process-Time-ms" in response.headers
    output = capsys.readouterr().out
    assert output.index("[store] setup") < output.index("[route]") < output.index("[background]") < output.index("[store] cleanup")
    assert modules["storage"].DELETION_LOG == ["Dune"]
    assert client.get("/books/1").status_code == 404

    response = client.get("/books", headers={"Origin": "http://localhost:5173"})
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_02_class4_recap(open_app, capsys):
    client, _ = open_app(HERE / "02_class4_recap")

    assert client.get("/items/1").json()["name"] == "Pen"
    assert client.get("/items/0").status_code == 422
    assert client.get("/items/99").status_code == 404

    assert client.get("/search?q=no").json()["results"][0]["name"] == "Notebook"
    assert client.get("/search?q=a").status_code == 422
    assert client.get("/search?q=pen&limit=99").status_code == 422

    assert [i["name"] for i in client.get("/filter?tag=gift&tag=kitchen").json()["results"]] == ["Mug", "Notebook"]
    assert client.get("/filter").status_code == 422

    response = client.get("/client-info", headers={"X-Client-Version": "2.1", "User-Agent": "pytest"})
    assert response.json() == {"client_version": "2.1", "user_agent": "pytest"}
    assert client.get("/client-info").status_code == 422

    assert client.get("/read-cookie").status_code == 401
    assert "session_id=abc123" in client.get("/set-cookie").headers["set-cookie"]
    assert client.get("/read-cookie").json() == {"session_id": "abc123"}

    assert client.post("/login", data={"username": "alice", "password": "wonderland"}).status_code == 200
    assert client.post("/login", data={"username": "alice", "password": "nope"}).status_code == 401
    assert client.post("/login", json={"username": "alice", "password": "wonderland"}).status_code == 422

    response = client.post("/upload", files={"file": ("cat.png", PNG_BYTES, "image/png")})
    assert response.json() == {"filename": "cat.png", "content_type": "image/png", "size": len(PNG_BYTES)}
    assert client.post("/upload", files={"file": ("notes.txt", b"hi", "text/plain")}).status_code == 400

    response = client.post("/items", json={"name": "Lamp", "price": 20})
    assert response.status_code == 201 and response.json()["id"] == 4
    assert client.post("/items", json={"name": "Lamp", "price": -1}).status_code == 422

    response = client.patch("/items/1", json={"price": 2.0})
    assert response.json()["name"] == "Pen" and response.json()["price"] == 2.0
    assert client.patch("/items/99", json={"price": 2.0}).status_code == 404

    body = {"email": "ada@example.com", "password": "supersecret", "confirm_password": "supersecret"}
    assert client.post("/register", json=body).status_code == 201
    assert client.post("/register", json=body).status_code == 409
    response = client.post("/register", json={**body, "email": "bo@example.com", "confirm_password": "different1"})
    assert response.status_code == 422 and "passwords do not match" in response.text

    assert client.get("/books?skip=10&limit=2").json()["items"] == ["Book 11", "Book 12"]
    assert client.get("/books?limit=50").status_code == 422
    assert client.get("/authors?skip=10").json()["items"] == ["Author 11", "Author 12"]
    assert client.get("/authors?skip=-1").status_code == 422

    capsys.readouterr()
    assert client.get("/reports/2025").json()["sales"] == 1850
    assert client.get("/reports/1999").status_code == 404
    output = capsys.readouterr().out
    assert output.count("[reports] open") == 2 and output.count("[reports] close") == 2

    assert client.get("/admin/stats", headers={"X-API-Key": TEST_API_KEY}).status_code == 200
    assert client.post("/admin/stats/reset", headers={"X-API-Key": TEST_API_KEY}).json() == {"visits": 0, "orders": 0}
    assert client.get("/admin/stats").status_code == 403
    assert client.get("/admin/stats", headers={"X-API-Key": "wrong"}).status_code == 403


def test_03_class6_recap(open_app, capsys):
    client, modules = open_app(HERE / "03_class6_recap")
    assert "admin created: admin@example.com" in capsys.readouterr().out

    response = register(client, "ana@example.com", "anapass123")
    assert response.status_code == 201 and response.json() == {"id": 2, "email": "ana@example.com", "role": "user"}
    assert modules["storage"].SENT_EMAILS == ["ana@example.com"]
    assert register(client, "ana@example.com", "anapass123").status_code == 409
    assert register(client, "bo@example.com", "short").status_code == 422

    ana = login_headers(client, "ana@example.com", "anapass123")
    admin = login_headers(client, "admin@example.com", "admin12345")
    assert client.post("/auth/login", data={"username": "ana@example.com", "password": "nope"}).status_code == 401

    assert client.get("/auth/me", headers=ana).json()["role"] == "user"
    assert client.get("/auth/me").status_code == 401
    expired = jwt.encode({"sub": "2", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)}, TEST_SECRET, algorithm="HS256")
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {expired}"}).status_code == 401

    assert len(client.get("/admin/users", headers=admin).json()) == 2
    assert client.get("/admin/users", headers=ana).status_code == 403
    assert client.get("/admin/emails", headers=admin).json() == ["ana@example.com"]
    assert client.get("/admin/emails", headers=ana).status_code == 403

    response = client.get("/auth/me", headers={**ana, "Origin": "http://localhost:5173"})
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert "X-Process-Time-ms" in response.headers
    response = client.get("/auth/me", headers={**ana, "Origin": "http://localhost:3000"})
    assert "access-control-allow-origin" not in response.headers


def bug_clients(open_app, bug: str) -> tuple[TestClient, TestClient, dict, dict]:
    buggy, buggy_modules = open_app(BUGS / bug / "buggy")
    fixed, fixed_modules = open_app(BUGS / bug / "fixed")
    return buggy, fixed, buggy_modules, fixed_modules


def test_bug_01_tags_filter(open_app):
    buggy, fixed, *_ = bug_clients(open_app, "bug_01_tags_filter")
    assert len(buggy.get("/filter?tag=music").json()["results"]) == 4
    assert "requestBody" in buggy.get("/openapi.json").json()["paths"]["/filter"]["get"]
    assert [p["name"] for p in fixed.get("/filter?tag=music").json()["results"]] == ["headphones", "guitar"]


def test_bug_02_partial_update(open_app):
    buggy, fixed, *_ = bug_clients(open_app, "bug_02_partial_update")
    assert buggy.patch("/items/1", json={"price": 2.0}).json() == {"id": 1, "name": None, "price": 2.0, "in_stock": None}
    assert fixed.patch("/items/1", json={"price": 2.0}).json() == {"id": 1, "name": "Pen", "price": 2.0, "in_stock": True}


def test_bug_03_depends_called(open_app):
    buggy, fixed, *_ = bug_clients(open_app, "bug_03_depends_called")
    assert buggy.get("/books?skip=10&limit=3").json()["items"] == [f"Book {n}" for n in range(1, 6)]
    assert buggy.get("/books?limit=500").status_code == 200
    assert fixed.get("/books?skip=10&limit=3").json()["items"] == ["Book 11", "Book 12", "Book 13"]
    assert fixed.get("/books?limit=500").status_code == 422


def test_bug_04_connection_cleanup(open_app):
    buggy, fixed, *_ = bug_clients(open_app, "bug_04_connection_cleanup")
    for client in (buggy, fixed):
        for _ in range(3):
            assert client.get("/books").status_code == 200
    assert buggy.get("/health").json() == {"open_connections": 3}
    assert fixed.get("/health").json() == {"open_connections": 0}


def test_bug_05_plain_password(open_app):
    buggy, fixed, *_ = bug_clients(open_app, "bug_05_plain_password")
    credentials = {"email": "ada@example.com", "password": "supersecret"}
    for client in (buggy, fixed):
        assert client.post("/auth/register", json=credentials).status_code == 201
        assert client.post("/auth/check-password", json=credentials).status_code == 200
        assert client.post("/auth/check-password", json={**credentials, "password": "wrongpass"}).status_code == 401
    assert buggy.get("/debug/storage").json()["ada@example.com"]["password"] == "supersecret"
    stored = fixed.get("/debug/storage").json()["ada@example.com"]
    assert "password" not in stored and stored["hashed_password"].startswith("$argon2id$")


def test_bug_06_login_messages(open_app):
    buggy, fixed, *_ = bug_clients(open_app, "bug_06_login_messages")

    def attempt(client, email):
        return client.post("/auth/login", data={"username": email, "password": "whatever"})

    unknown, wrong = attempt(buggy, "nobody@example.com"), attempt(buggy, "ada@example.com")
    assert (unknown.status_code, wrong.status_code) == (404, 401) and unknown.json() != wrong.json()
    unknown, wrong = attempt(fixed, "nobody@example.com"), attempt(fixed, "ada@example.com")
    assert unknown.status_code == wrong.status_code == 401 and unknown.json() == wrong.json()
    assert fixed.post("/auth/login", data={"username": "ada@example.com", "password": "supersecret"}).status_code == 200


def test_bug_07_admin_401(open_app):
    buggy, fixed, *_ = bug_clients(open_app, "bug_07_admin_401")
    for client in (buggy, fixed):
        assert client.delete("/books/1").status_code == 401
        assert client.delete("/books/1", headers={"X-Token": "admin-token"}).status_code == 204
    assert buggy.delete("/books/2", headers={"X-Token": "user-token"}).status_code == 401
    assert fixed.delete("/books/2", headers={"X-Token": "user-token"}).status_code == 403


def test_bug_08_secret_in_code(open_app, monkeypatch):
    buggy, fixed, buggy_modules, fixed_modules = bug_clients(open_app, "bug_08_secret_in_code")
    leaked_key = buggy_modules["security"].SECRET_KEY
    forged = jwt.encode({"sub": "1", "exp": datetime.now(timezone.utc) + timedelta(minutes=5)}, leaked_key, algorithm="HS256")
    forged_headers = {"Authorization": f"Bearer {forged}"}

    assert buggy.get("/auth/me", headers=forged_headers).json() == {"user_id": 1, "is_admin": True}
    assert fixed.get("/auth/me", headers=forged_headers).status_code == 401
    assert fixed.get("/auth/me", headers=login_headers(fixed, "ada@example.com", "supersecret")).json()["user_id"] == 2
    assert not hasattr(fixed_modules["security"], "SECRET_KEY")

    monkeypatch.delenv("SECRET_KEY")
    with pytest.raises(ValidationError, match="secret_key"):
        fixed_modules["config"].Settings(_env_file=None)


def test_bug_09_cors_origin(open_app):
    buggy, fixed, *_ = bug_clients(open_app, "bug_09_cors_origin")
    preflight = {"Origin": "http://localhost:5173", "Access-Control-Request-Method": "GET"}
    assert buggy.options("/books", headers=preflight).status_code == 400
    assert "access-control-allow-origin" not in buggy.get("/books", headers={"Origin": "http://localhost:5173"}).headers
    response = fixed.options("/books", headers=preflight)
    assert response.status_code == 200 and response.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert fixed.get("/books", headers={"Origin": "http://localhost:5173"}).headers["access-control-allow-origin"] == "http://localhost:5173"


def test_05_notes_starter_starts(open_app):
    client, _ = open_app(HERE / "05_notes_api_challenge" / "starter")
    paths = client.get("/openapi.json").json()["paths"]
    assert {"/auth/register", "/auth/login", "/auth/me", "/notes", "/notes/{note_id}"} <= set(paths)


def test_05_notes_solution(open_app, capsys):
    client, modules = open_app(HERE / "05_notes_api_challenge" / "solution")
    assert register(client, "ana@example.com", "anapass123").status_code == 201
    assert register(client, "ben@example.com", "benpass123").status_code == 201
    assert register(client, "ana@example.com", "anapass123").status_code == 409
    assert register(client, "cy@example.com", "short").status_code == 422
    assert client.post("/auth/login", data={"username": "ana@example.com", "password": "nope"}).status_code == 401
    ana = login_headers(client, "ana@example.com", "anapass123")
    ben = login_headers(client, "ben@example.com", "benpass123")
    admin = login_headers(client, "admin@example.com", "admin12345")
    assert client.get("/auth/me", headers=ana).json()["email"] == "ana@example.com"

    ana_note = client.post("/notes", json={"title": "Shopping", "content": "milk, eggs"}, headers=ana)
    assert ana_note.status_code == 201 and ana_note.json()["owner_id"] == 2
    client.post("/notes", json={"title": "Ana diary", "content": "dear diary"}, headers=ana)
    ben_note = client.post("/notes", json={"title": "Ben ideas", "content": "start a band"}, headers=ben).json()
    assert modules["storage"].NOTE_EVENTS[0] == "note 1 created by ana@example.com"

    assert [n["title"] for n in client.get("/notes", headers=ana).json()] == ["Shopping", "Ana diary"]
    assert [n["title"] for n in client.get("/notes", headers=ben).json()] == ["Ben ideas"]
    assert [n["title"] for n in client.get("/notes?q=milk", headers=ana).json()] == ["Shopping"]
    assert [n["title"] for n in client.get("/notes?skip=1&limit=1", headers=ana).json()] == ["Ana diary"]
    assert client.get("/notes?q=a", headers=ana).status_code == 422

    assert client.get(f"/notes/{ben_note['id']}", headers=ana).status_code == 403
    assert client.get("/notes/1", headers=ben).status_code == 403
    assert client.patch("/notes/1", json={"title": "Hacked"}, headers=ben).status_code == 403
    assert client.delete("/notes/1", headers=ben).status_code == 403

    response = client.patch("/notes/1", json={"content": "milk, eggs, bread"}, headers=ana)
    assert response.json()["title"] == "Shopping" and response.json()["content"] == "milk, eggs, bread"

    response = client.get("/notes/99", headers=ana)
    assert response.status_code == 404 and response.json() == {"error": "NoteNotFound", "message": "Note 99 does not exist"}
    assert client.get("/notes").status_code == 401

    assert client.delete(f"/notes/{ben_note['id']}", headers=admin).status_code == 204
    assert client.delete("/notes/1", headers=admin).status_code == 204
    assert client.get("/notes", headers=ben).json() == []
    assert client.delete("/notes/2", headers=ana).status_code == 204

    response = client.get("/notes", headers={**ana, "Origin": "http://localhost:5173"})
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert "X-Process-Time-ms" in response.headers
    assert "GET /notes -> 200" in capsys.readouterr().out
