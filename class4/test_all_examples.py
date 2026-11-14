import importlib
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

HERE = Path(__file__).parent
SAMPLES = HERE / "sample_files"


def load_module(folder: Path, module: str = "main"):
    before = set(sys.modules)
    sys.path.insert(0, str(folder))
    try:
        return importlib.import_module(module)
    finally:
        sys.path.remove(str(folder))
        for name in set(sys.modules) - before:
            file = getattr(sys.modules[name], "__file__", None) or ""
            if file.startswith(str(folder)):
                del sys.modules[name]


def client_for(folder: str, module: str = "main") -> TestClient:
    return TestClient(load_module(HERE / folder, module).app)


def upload(name: str, content_type: str):
    return (name, (SAMPLES / name).read_bytes(), content_type)


def test_01_query_validation():
    c = client_for("01_query_validation")
    r = c.get("/search", params={"q": "lap"})
    assert r.status_code == 200 and r.json()["results"][0]["name"] == "laptop"
    r = c.get("/filter?tag=music&tag=school")
    assert [p["name"] for p in r.json()["results"]] == ["headphones", "notebook", "guitar"]
    assert c.get("/greet?name=Ada").json() == {"message": "Hello, Ada!"}
    assert c.get("/search?q=a").status_code == 422
    assert c.get("/search?limit=100").status_code == 422
    assert c.get("/greet").status_code == 422


def test_02_path_validation():
    c = client_for("02_path_validation")
    assert c.get("/items/1").json() == {"id": 1, "name": "Keyboard"}
    assert c.get("/users/ada_99").status_code == 200
    assert c.get("/items/0").status_code == 422
    assert c.get("/items/5000").status_code == 422
    assert c.get("/items/abc").status_code == 422
    assert c.get("/items/42").status_code == 404
    assert c.get("/users/Ab").status_code == 422


def test_03_headers_cookies():
    c = client_for("03_headers_cookies")
    r = c.get("/headers", headers={"User-Agent": "pytest", "X-Token": "hello"})
    assert r.json() == {"user_agent": "pytest", "x_token": "hello"}
    assert c.get("/secure", headers={"X-Token": "secret-token"}).status_code == 200
    assert c.get("/secure").status_code == 422
    assert c.get("/secure", headers={"X-Token": "wrong"}).status_code == 401
    assert c.get("/read-cookie").status_code == 401
    r = c.get("/set-cookie")
    assert "session_id=abc123" in r.headers["set-cookie"]
    assert c.get("/read-cookie").json() == {"session_id": "abc123"}
    c.get("/clear-cookie")
    assert c.get("/read-cookie").status_code == 401


def test_04_form_and_upload():
    c = client_for("04_form_and_upload")
    assert c.post("/login", data={"username": "alice", "password": "wonderland"}).status_code == 200
    assert c.post("/login", data={"username": "alice", "password": "nope"}).status_code == 401
    assert c.post("/login", data={"username": "alice", "password": "abc"}).status_code == 422
    assert c.post("/login", json={"username": "alice", "password": "wonderland"}).status_code == 422

    r = c.post("/upload", files={"file": upload("cat.png", "image/png")})
    assert r.json() == {"filename": "cat.png", "content_type": "image/png", "size": 69}
    assert (HERE / "04_form_and_upload/uploads/cat.png").exists()
    assert c.post("/upload", files={"file": upload("notes.txt", "text/plain")}).status_code == 400

    files = [("files", upload("cat.png", "image/png")), ("files", upload("dog.jpg", "image/jpeg"))]
    r = c.post("/upload-many", files=files)
    assert [f["filename"] for f in r.json()["uploaded"]] == ["cat.png", "dog.jpg"]
    files.append(("files", upload("notes.txt", "text/plain")))
    assert c.post("/upload-many", files=files).status_code == 400


def test_05_patch_partial_update():
    c = client_for("05_patch_partial_update")
    r = c.patch("/items/1", json={"price": 2.0})
    assert r.json() == {"name": "Pen", "price": 2.0, "in_stock": True}
    r = c.put("/items/2", json={"name": "Big Mug", "price": 9.0})
    assert r.json() == {"name": "Big Mug", "price": 9.0, "in_stock": True}
    r = c.patch("/items/1/broken", json={"price": 9.9})
    assert r.json()["item_would_become"] == {"name": None, "price": 9.9, "in_stock": None}
    assert c.get("/items/1").json()["name"] == "Pen"
    assert c.put("/items/1", json={"price": 3.0}).status_code == 422
    assert c.patch("/items/99", json={"price": 1.0}).status_code == 404
    assert c.patch("/items/1", json={"price": "cheap"}).status_code == 422


def test_06_model_validator_email():
    c = client_for("06_model_validator_email")
    good = {"email": "ada@example.com", "password": "supersecret", "confirm_password": "supersecret"}
    assert c.post("/register", json=good).status_code == 201
    assert c.post("/register", json=good).status_code == 400
    assert c.post("/register", json={**good, "email": "not-an-email"}).status_code == 422
    r = c.post("/register", json={**good, "password": "short", "confirm_password": "short"})
    assert r.status_code == 422 and "at least 8" in r.text
    r = c.post("/register", json={**good, "email": "bob@example.com", "confirm_password": "different1"})
    assert r.status_code == 422 and "do not match" in r.text


def test_07_status_and_list_response():
    c = client_for("07_status_and_list_response")
    users = c.get("/users").json()
    assert len(users) == 2 and all("password" not in u for u in users)
    r = c.post("/users", json={"username": "cara", "email": "cara@example.com", "password": "pw"})
    assert r.status_code == 201 and r.json() == {"id": 3, "username": "cara", "email": "cara@example.com"}
    r = c.delete("/users/2")
    assert r.status_code == 204 and r.content == b""
    assert c.delete("/users/2").status_code == 404
    assert c.get("/users/99").status_code == 404
    assert c.post("/users", json={"username": "dan"}).status_code == 422


def test_08_custom_exceptions():
    c = client_for("08_custom_exceptions")
    assert c.get("/books/1").status_code == 200
    assert c.post("/books/1/buy").json()["stock_left"] == 1
    r = c.get("/books/99")
    assert r.status_code == 404 and r.json() == {"error": "BookNotFound", "message": "Book 99 does not exist"}
    r = c.post("/books/2/buy")
    assert r.status_code == 409 and r.json()["error"] == "OutOfStock"


def test_09_depends_basics():
    c = client_for("09_depends_basics")
    assert c.get("/books").json()["items"] == [f"Book {n}" for n in range(1, 6)]
    assert c.get("/books?skip=10&limit=3").json()["items"] == ["Book 11", "Book 12", "Book 13"]
    assert c.get("/authors?skip=10").json()["items"] == ["Author 11", "Author 12"]
    assert c.get("/books?limit=50").status_code == 422
    assert c.get("/authors?skip=-1").status_code == 422


def test_10_class_and_sub_dependencies():
    c = client_for("10_class_and_sub_dependencies")
    assert c.get("/products?skip=2&limit=2").json()["items"] == ["cherry", "date"]
    assert c.get("/me", headers={"X-Token": "alice-token"}).json() == {"username": "alice", "role": "admin"}
    r = c.get("/my-products?limit=1", headers={"X-Token": "bob-token"})
    assert r.json() == {"user": "bob", "items": ["apple"]}
    r = c.get("/me")
    assert r.status_code == 401 and r.json()["detail"] == "Missing X-Token header"
    r = c.get("/me", headers={"X-Token": "hacker"})
    assert r.status_code == 401 and r.json()["detail"] == "Invalid token"
    assert c.get("/products?limit=0").status_code == 422


def test_11_yield_dependency(capsys):
    c = client_for("11_yield_dependency")
    assert c.get("/books").status_code == 200
    out = capsys.readouterr().out
    assert out.index("OPEN") < out.index("route running") < out.index("CLOSE")
    assert "ROLLBACK" not in out

    assert c.get("/books/99").status_code == 404
    out = capsys.readouterr().out
    assert out.index("OPEN") < out.index("route running") < out.index("ROLLBACK") < out.index("CLOSE")


def test_12_router_level_dependencies():
    c = client_for("12_router_level_dependencies")
    assert c.get("/public/hello").status_code == 200
    assert c.get("/public/books").status_code == 200
    key = {"X-API-Key": "super-secret-key"}
    assert c.get("/admin/stats", headers=key).json() == {"users": 42, "orders": 7}
    assert c.post("/admin/reset", headers=key).status_code == 200
    assert c.get("/admin/stats").status_code == 403
    assert c.get("/admin/stats", headers={"X-API-Key": "wrong"}).status_code == 403


def test_13_bookstore():
    c = client_for("13_mini_project_bookstore")
    key = {"X-API-Key": "bookstore-admin-key"}

    books = c.get("/books?limit=2").json()
    assert [b["title"] for b in books] == ["Dune", "1984"]
    assert all("cost_price" not in b for b in books)
    assert [b["title"] for b in c.get("/books?author_id=2").json()] == ["1984", "Animal Farm"]

    new = {"title": "Brave New World", "author_id": 2, "price": 9, "cost_price": 4}
    r = c.post("/books", json=new)
    assert r.status_code == 201 and r.json()["id"] == 5 and "cost_price" not in r.json()
    r = c.patch("/books/1", json={"price": 12.5})
    assert r.json()["price"] == 12.5 and r.json()["title"] == "Dune"

    r = c.post("/books/1/cover", files={"file": upload("cat.png", "image/png")})
    assert r.json()["cover"] == "book_1.png"
    assert (HERE / "13_mini_project_bookstore/uploads/book_1.png").exists()

    assert c.post("/authors", json={"name": "Ursula K. Le Guin"}).status_code == 201
    assert len(c.get("/authors/2/books").json()) == 3

    assert c.get("/admin/stats", headers=key).json()["books"] == 5
    assert c.delete("/admin/books/4", headers=key).status_code == 204
    assert c.get("/books/4").status_code == 404

    r = c.get("/books/99")
    assert r.status_code == 404 and r.json() == {"error": "BookNotFound", "message": "Book 99 not found"}
    assert c.get("/books/0").status_code == 422
    r = c.post("/books", json={**new, "author_id": 99})
    assert r.status_code == 404 and r.json()["error"] == "AuthorNotFound"
    assert c.get("/authors/99").json()["error"] == "AuthorNotFound"
    assert c.patch("/books/1", json={"price": -1}).status_code == 422
    assert c.post("/books/1/cover", files={"file": upload("notes.txt", "text/plain")}).status_code == 400
    assert c.get("/admin/stats").status_code == 403
    assert c.delete("/admin/books/1", headers={"X-API-Key": "wrong"}).status_code == 403


PRACTICE = HERE / "practice"


@pytest.mark.parametrize("path", sorted(PRACTICE.glob("task*.py")), ids=lambda p: p.stem)
def test_practice_starters_import(path):
    assert load_module(PRACTICE, path.stem).app


def sol(name: str) -> TestClient:
    return client_for("practice/solutions", name)


def test_solutions_query_and_path():
    c = sol("task01_search")
    assert c.get("/search?q=ap").json()["results"] == ["apple", "apricot"]
    assert c.get("/search?q=a").status_code == 422
    c = sol("task02_page_size")
    assert len(c.get("/numbers?page_size=5").json()["items"]) == 5
    assert c.get("/numbers?page_size=51").status_code == 422
    c = sol("task03_book_id")
    assert c.get("/books/1").status_code == 200
    assert c.get("/books/0").status_code == 422
    assert c.get("/books/7").status_code == 404
    c = sol("task04_filter_genres")
    assert c.get("/filter?genre=scifi&genre=horror").json() == {"genres": ["scifi", "horror"]}
    assert c.get("/filter").status_code == 422


def test_solutions_headers_upload_patch_signup():
    c = sol("task05_whoami")
    assert c.get("/whoami", headers={"User-Agent": "pytest"}).json() == {"user_agent": "pytest"}
    assert c.get("/whoami", headers={"User-Agent": ""}).status_code == 400
    c = sol("task06_avatar")
    assert c.post("/avatar", files={"file": upload("dog.jpg", "image/jpeg")}).status_code == 200
    assert c.post("/avatar", files={"file": upload("notes.txt", "text/plain")}).status_code == 400
    c = sol("task07_patch_book")
    r = c.patch("/books/1", json={"price": 5})
    assert r.json() == {"title": "Dune", "author": "Frank Herbert", "price": 5.0}
    assert c.patch("/books/9", json={"price": 5}).status_code == 404
    c = sol("task08_signup")
    good = {"email": "a@example.com", "password": "pw123456", "confirm_password": "pw123456"}
    assert c.post("/signup", json=good).status_code == 201
    assert c.post("/signup", json={**good, "confirm_password": "x"}).status_code == 422
    assert c.post("/signup", json={**good, "email": "nope"}).status_code == 422


def test_solutions_exceptions_and_dependencies(capsys):
    c = sol("task09_author_not_found")
    assert c.get("/authors/1").status_code == 200
    assert c.get("/authors/9").json() == {"error": "AuthorNotFound", "message": "Author 9 not found"}
    for name in ("task10_pagination_dependency", "task11_pagination_class"):
        c = sol(name)
        assert c.get("/books?skip=5&limit=2").json() == ["Book 6", "Book 7"]
        assert c.get("/authors?limit=99").status_code == 422
    c = sol("task12_get_db_yield")
    assert c.get("/books/9").status_code == 404
    out = capsys.readouterr().out
    assert out.index("DB OPEN") < out.index("DB CLOSE")
    c = sol("task13_admin_router")
    assert c.get("/").status_code == 200
    assert c.get("/admin/dashboard", headers={"X-API-Key": "letmein"}).status_code == 200
    assert c.get("/admin/dashboard").status_code == 403
