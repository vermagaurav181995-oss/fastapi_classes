"""
Tests for every Class 6 example.

Run from the class6/ folder:   pytest -v test_all_examples.py

How it works
* SECRET_KEY comes from an environment variable (no .env file needed).
* Every test gets its OWN temporary SQLite file: DATABASE_URL points to it, and
  app.dependency_overrides[get_db] hands the routes sessions on that same file.
* Each example folder has its own config.py / database.py / routers/ ..., so
  load_example() imports them in isolation and forgets them afterwards.
"""

import importlib
import os
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import jwt
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

HERE = Path(__file__).parent
TEST_SECRET = "test-secret-" + "k" * 52
os.environ["SECRET_KEY"] = TEST_SECRET


def load_example(folder: Path, module: str = "main") -> dict:
    """Import `module` from `folder`; return every module it loaded from that folder."""
    before = set(sys.modules)
    sys.path.insert(0, str(folder))
    try:
        importlib.import_module(module)
    finally:
        sys.path.remove(str(folder))
    loaded = {}
    for name in set(sys.modules) - before:
        mod = sys.modules[name]
        if (getattr(mod, "__file__", None) or "").startswith(str(folder)):
            loaded[name] = sys.modules.pop(name)  # forget it so the next example is clean
    return loaded


@pytest.fixture
def example(tmp_path, monkeypatch):
    """example("05_login") -> SimpleNamespace(client, main, db_session, modules)."""
    opened = []

    def _make(folder: str, module: str = "main", env: dict | None = None):
        db_url = f"sqlite:///{tmp_path / f'test_{uuid.uuid4().hex[:8]}.db'}"  # fresh DB per app
        monkeypatch.setenv("DATABASE_URL", db_url)
        for key, value in (env or {}).items():
            monkeypatch.setenv(key, value)
        mods = load_example(HERE / folder, module)
        main = mods[module]
        ns = SimpleNamespace(main=main, modules=mods, db_session=None)

        database = mods.get("database") or (mods.get("common") if hasattr(mods.get("common"), "get_db") else None)
        if database is not None:
            engine = create_engine(db_url, connect_args={"check_same_thread": False})
            database.Base.metadata.create_all(engine)
            TestSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

            def override_get_db():
                db = TestSession()
                try:
                    yield db
                finally:
                    db.close()

            main.app.dependency_overrides[database.get_db] = override_get_db
            ns.db_session = TestSession
            opened.append(engine.dispose)

        client = TestClient(main.app)
        client.__enter__()  # runs the lifespan (startup)
        opened.append(lambda: client.__exit__(None, None, None))
        ns.client = client
        return ns

    yield _make
    for close in reversed(opened):
        close()


# ------------------------------------------------------------------ helpers
def register(c, email="ada@example.com", password="supersecret"):
    return c.post("/auth/register", json={"email": email, "password": password})


def login(c, email="ada@example.com", password="supersecret"):
    return c.post("/auth/login", data={"username": email, "password": password})


def bearer(c, email="ada@example.com", password="supersecret") -> dict:
    r = login(c, email, password)
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def expired_bearer(user_id: int = 1) -> dict:
    payload = {"sub": str(user_id), "exp": datetime.now(timezone.utc) - timedelta(minutes=1)}
    return {"Authorization": f"Bearer {jwt.encode(payload, TEST_SECRET, algorithm='HS256')}"}


FAKE = {"Authorization": "Bearer fake.token.value"}


# ======================================================================== 01
def test_01_password_hashing(example):
    c = example("01_password_hashing").client
    data = c.get("/demo/hash?password=secret123").json()
    assert data["hash_1"].startswith("$argon2id$")
    assert data["hashes_are_equal"] is False and data["both_verify"] is True
    assert c.get("/demo/verify?password=secret123&attempt=secret123").json()["is_valid"] is True
    assert c.get("/demo/verify?password=secret123&attempt=wrong").json()["is_valid"] is False
    assert c.get("/demo/hash?password=").status_code == 422


# ======================================================================== 02
def test_02_settings_secret_key(example, monkeypatch):
    ex = example("02_settings_secret_key")
    data = ex.client.get("/settings").json()
    assert data["algorithm"] == "HS256" and data["secret_key_length"] == len(TEST_SECRET)
    assert ex.client.get("/settings/secret_key").status_code == 404
    # Without SECRET_KEY the Settings class refuses to load
    monkeypatch.delenv("SECRET_KEY")
    with pytest.raises(ValidationError, match="secret_key"):
        ex.modules["config"].Settings(_env_file=None)


# ======================================================================== 03
def test_03_register(example):
    c = example("03_user_model_register").client
    r = register(c)
    assert r.status_code == 201
    assert r.json() == {"id": 1, "email": "ada@example.com", "role": "user", "is_active": True}
    assert "password" not in r.text and "argon2" not in r.text
    assert register(c).status_code == 409
    assert register(c, "ada2@example.com", "short").status_code == 422
    assert register(c, "not-an-email").status_code == 422


# ======================================================================== 04
def test_04_jwt(example):
    c = example("04_jwt_create_decode").client
    token = c.get("/demo/token?user_id=7").json()["access_token"]
    payload = c.get("/demo/decode", params={"token": token}).json()["payload"]
    assert payload["sub"] == "7" and "exp" in payload
    r = c.get("/demo/tampered")
    assert r.status_code == 401 and "Signature verification failed" in r.json()["detail"]
    r = c.get("/demo/expired")
    assert r.status_code == 401 and r.json()["detail"] == "Token has expired"
    assert c.get("/demo/decode?token=abc").status_code == 401
    assert c.get("/demo/token?user_id=0").status_code == 422


# ======================================================================== 05
def test_05_login(example):
    c = example("05_login").client
    user_id = register(c).json()["id"]
    r = login(c)
    assert r.status_code == 200 and r.json()["token_type"] == "bearer"
    payload = jwt.decode(r.json()["access_token"], TEST_SECRET, algorithms=["HS256"])
    assert payload["sub"] == str(user_id)

    wrong_pw = login(c, password="wrongpass")
    unknown = login(c, email="nobody@example.com")
    assert wrong_pw.status_code == unknown.status_code == 401
    assert wrong_pw.json() == unknown.json() == {"detail": "Incorrect email or password"}
    assert wrong_pw.headers["www-authenticate"] == "Bearer"
    assert c.post("/auth/login", json={"username": "ada@example.com", "password": "supersecret"}).status_code == 422


# ======================================================================== 06
def test_06_me(example):
    ex = example("06_get_current_user_me")
    c = ex.client
    register(c)
    r = c.get("/auth/me", headers=bearer(c))
    assert r.status_code == 200 and r.json()["email"] == "ada@example.com"

    no_token = c.get("/auth/me")
    assert no_token.status_code == 401 and no_token.json()["detail"] == "Not authenticated"
    assert c.get("/auth/me", headers=FAKE).status_code == 401
    expired = c.get("/auth/me", headers=expired_bearer(1))
    assert expired.status_code == 401 and expired.json()["detail"] == "Could not validate credentials"

    # A deactivated user is refused even with a valid token
    headers = bearer(c)
    with ex.db_session() as db:
        db.get(ex.modules["models"].User, 1).is_active = False
        db.commit()
    assert c.get("/auth/me", headers=headers).status_code == 403


# ======================================================================== 07
def test_07_protect_router(example):
    c = example("07_protect_router").client
    assert c.get("/public/info").status_code == 200
    assert c.get("/books").status_code == 401
    assert c.get("/books/1", headers=FAKE).status_code == 401
    assert c.post("/books", json={"title": "X"}).status_code == 401
    register(c)
    h = bearer(c)
    assert len(c.get("/books", headers=h).json()) == 2
    r = c.post("/books", json={"title": "Neuromancer"}, headers=h)
    assert r.status_code == 201 and r.json()["added_by"] == "ada@example.com"
    assert c.get("/books/99", headers=h).status_code == 404


# ======================================================================== 08
def test_08_roles(example):
    c = example("08_roles_require_role").client
    user = bearer(c, "user@example.com", "user12345")
    admin = bearer(c, "admin@example.com", "admin12345")
    assert c.get("/books").status_code == 200
    assert c.post("/books", json={"title": "Emma"}, headers=user).status_code == 201
    r = c.delete("/books/1", headers=user)
    assert r.status_code == 403 and r.json()["detail"] == "Not enough permissions"
    assert c.delete("/books/1").status_code == 401
    r = c.delete("/books/1", headers=admin)
    assert r.status_code == 204 and r.content == b""
    assert c.delete("/books/999", headers=admin).status_code == 404


# ======================================================================== 09
def test_09_ownership(example):
    c = example("09_ownership_check").client
    alice = bearer(c, "alice@example.com", "alice12345")
    admin = bearer(c, "admin@example.com", "admin12345")
    assert c.patch("/reviews/1", json={"rating": 3}, headers=alice).json()["rating"] == 3
    r = c.patch("/reviews/2", json={"rating": 1}, headers=alice)
    assert r.status_code == 403 and "own reviews" in r.json()["detail"]
    assert c.delete("/reviews/2", headers=alice).status_code == 403
    assert c.patch("/reviews/2", json={"rating": 1}).status_code == 401
    assert c.patch("/reviews/2", json={"text": "Edited by admin"}, headers=admin).status_code == 200
    new = c.post("/reviews", json={"book_title": "Emma", "text": "Lovely", "rating": 4}, headers=alice)
    assert new.status_code == 201 and new.json()["owner_id"] == 2
    assert c.post("/reviews", json={"book_title": "Emma", "text": "x", "rating": 9}, headers=alice).status_code == 422
    assert c.delete("/reviews/1", headers=alice).status_code == 204


# ======================================================================== 10
def test_10_change_password(example):
    c = example("10_change_password").client
    register(c)
    h = bearer(c)
    body = {"old_password": "supersecret", "new_password": "evenmoresecret"}
    assert c.patch("/auth/me/password", json={**body, "old_password": "WRONG"}, headers=h).status_code == 400
    assert c.patch("/auth/me/password", json={**body, "new_password": "short"}, headers=h).status_code == 422
    assert c.patch("/auth/me/password", json=body).status_code == 401
    assert c.patch("/auth/me/password", json=body, headers=h).status_code == 200
    assert login(c, password="supersecret").status_code == 401
    assert login(c, password="evenmoresecret").status_code == 200


# ======================================================================== 11
def test_11_cors(example):
    c = example("11_cors").client
    preflight = {"Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST"}
    r = c.options("/auth/login", headers=preflight)
    assert r.status_code == 200
    assert r.headers["access-control-allow-origin"] == "http://localhost:5173"

    h = {**bearer(c, "student@example.com", "password123"), "Origin": "http://localhost:3000"}
    r = c.get("/auth/me", headers=h)
    assert r.status_code == 200 and r.headers["access-control-allow-origin"] == "http://localhost:3000"

    r = c.options("/auth/login", headers={**preflight, "Origin": "http://evil.example"})
    assert r.status_code == 400 and "access-control-allow-origin" not in r.headers
    r = c.get("/auth/me", headers={"Origin": "http://evil.example"})
    assert r.status_code == 401 and "access-control-allow-origin" not in r.headers


# ======================================================================== 12
def test_12_middleware(example, capsys):
    c = example("12_custom_middleware").client
    r = c.get("/")
    assert r.status_code == 200
    assert float(r.headers["X-Process-Time-ms"]) >= 0
    assert str(uuid.UUID(r.headers["X-Request-ID"])) == r.json()["request_id"]
    out = capsys.readouterr().out
    assert out.index("[request-id] start") < out.index("[timing]     before") < out.index("[route]")
    assert out.index("GET / -> 200") < out.index("[request-id] end")

    r = c.get("/items/99")
    assert r.status_code == 404 and "X-Process-Time-ms" in r.headers and "X-Request-ID" in r.headers
    assert c.get("/items/abc").status_code == 422


# ======================================================================== 13
def test_13_background_tasks(example):
    ex = example("13_background_tasks")
    ex.main.EMAIL_DELAY_SECONDS = 0  # don't make the test wait 3 seconds
    c = ex.client
    assert register(c).status_code == 201
    # TestClient runs background tasks before returning, so it already ran:
    assert c.get("/emails/sent").json() == ["ada@example.com"]
    assert register(c).status_code == 409
    assert register(c, "x@example.com", "short").status_code == 422
    assert ex.main.SENT_EMAILS == ["ada@example.com"]  # no email for failed requests


# ======================================================================== 14
def test_14_lifespan(example, capsys):
    env = {"ADMIN_EMAIL": "admin@example.com", "ADMIN_PASSWORD": "admin12345"}
    ex = example("14_lifespan", env=env)
    c = ex.client
    assert "created first admin: admin@example.com" in capsys.readouterr().out
    admin = bearer(c, "admin@example.com", "admin12345")
    assert c.get("/auth/me", headers=admin).json()["role"] == "admin"
    assert c.get("/admin/users", headers=admin).status_code == 200

    assert register(c, "ana@example.com", "anapass123").status_code == 201
    assert c.get("/admin/users", headers=bearer(c, "ana@example.com", "anapass123")).status_code == 403
    assert c.get("/admin/users").status_code == 401
    assert register(c, "admin@example.com", "whatever123").status_code == 409

    # A second startup must NOT create another admin
    with TestClient(ex.main.app):
        pass
    out = capsys.readouterr().out
    assert "an admin already exists" in out and "SHUTDOWN" in out


# ======================================================================== 15
def test_15_bookstore(example, capsys):
    env = {"ADMIN_EMAIL": "admin@example.com", "ADMIN_PASSWORD": "admin12345"}
    c = example("15_bookstore_full", env=env).client

    r = c.get("/books", headers={"Origin": "http://localhost:5173"})
    assert [b["title"] for b in r.json()] == ["Dune", "1984", "Animal Farm"]
    assert r.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert "X-Process-Time-ms" in r.headers
    assert c.get("/authors/2/books").status_code == 200

    assert register(c).status_code == 201
    assert "welcome email sent to ada@example.com" in capsys.readouterr().out
    r = register(c)
    assert r.status_code == 409 and r.json()["error"] == "Conflict"
    assert register(c, "b@example.com", "short").status_code == 422
    assert login(c, password="nope").status_code == 401

    user, admin = bearer(c), bearer(c, "admin@example.com", "admin12345")
    assert c.post("/books", json={"title": "Emma", "author_id": 1}).status_code == 401
    assert c.post("/books", json={"title": "Emma", "year": 1815, "author_id": 1}, headers=user).status_code == 201
    r = c.post("/books", json={"title": "Ghost", "author_id": 99}, headers=user)
    assert r.status_code == 404 and r.json() == {"error": "NotFound", "message": "Author 99 not found"}
    assert c.post("/authors", json={"name": "Jane Austen"}, headers=user).status_code == 201
    assert c.post("/authors", json={"name": "Jane Austen"}, headers=user).status_code == 409

    review = c.post("/books/1/reviews", json={"rating": 5, "text": "Great"}, headers=admin).json()
    assert c.patch(f"/reviews/{review['id']}", json={"rating": 1}, headers=user).status_code == 403
    mine = c.post("/books/1/reviews", json={"rating": 4, "text": "Nice"}, headers=user).json()
    assert c.patch(f"/reviews/{mine['id']}", json={"rating": 2}, headers=user).json()["rating"] == 2

    assert c.delete("/books/3", headers=user).status_code == 403
    assert c.delete("/books/3", headers=admin).status_code == 204
    assert c.get("/books/3").json()["error"] == "NotFound"
    assert c.delete("/authors/1", headers=admin).status_code == 204
    assert c.get("/books/1").status_code == 404  # cascade removed Dune
    assert c.get("/auth/me", headers=expired_bearer(2)).status_code == 401
    assert c.patch("/auth/me/password", json={"old_password": "x", "new_password": "newpass123"}, headers=user).status_code == 400


# ================================================================== practice
PRACTICE = HERE / "practice"


@pytest.mark.parametrize("path", sorted(PRACTICE.glob("task*.py")), ids=lambda p: p.stem)
def test_practice_starter_loads(example, path):
    """Starters are unfinished on purpose, but they must import and start."""
    assert example("practice", path.stem).client.get("/openapi.json").status_code == 200


def solution(example, name, **kw):
    return example("practice/solutions", name, **kw)


def test_solution_01_to_03(example, monkeypatch):
    ex = solution(example, "task01_secret_key")
    assert ex.client.get("/check").json()["secret_key_loaded"] is True
    monkeypatch.delenv("SECRET_KEY")
    with pytest.raises(ValidationError):
        ex.main.Settings(_env_file=None)
    monkeypatch.setenv("SECRET_KEY", TEST_SECRET)

    cols = solution(example, "task02_user_model").client.get("/columns").json()
    assert set(cols) == {"id", "email", "hashed_password", "role", "is_active"} and cols["email"]["unique"]

    c = solution(example, "task03_hashing").client
    assert c.get("/hash-twice").json()["equal"] is False
    assert c.get("/verify?password=a&attempt=b").json()["is_valid"] is False


def test_solution_04_05(example, capsys):
    c = solution(example, "task04_register").client
    r = register(c)
    assert r.status_code == 201 and "hash" not in r.text
    assert register(c).status_code == 409

    c = solution(example, "task05_login").client
    assert login(c, "student@example.com", "password123").status_code == 200
    assert "token payload: {'sub':" in capsys.readouterr().out
    assert login(c, "student@example.com", "wrong").status_code == 401


def test_solution_06_to_08(example):
    for name in ("task06_me", "task07_token_expiry"):
        c = solution(example, name).client
        assert c.get("/auth/me").status_code == 401
        assert c.get("/auth/me", headers=FAKE).status_code == 401
        assert c.get("/auth/me", headers=expired_bearer(1)).status_code == 401
        assert c.get("/auth/me", headers=bearer(c, "student@example.com", "password123")).status_code == 200
    assert "exp" in c.get("/auth/token-info", headers=bearer(c, "student@example.com", "password123")).json()

    c = solution(example, "task08_protect_router").client
    assert c.get("/books").status_code == 401
    assert c.get("/books/count", headers=bearer(c, "student@example.com", "password123")).status_code == 200


def test_solution_09_10(example):
    c = solution(example, "task09_require_role").client
    assert c.delete("/books/1", headers=bearer(c, "student@example.com", "password123")).status_code == 403
    assert c.delete("/books/1", headers=bearer(c, "admin@example.com", "admin12345")).status_code == 204

    c = solution(example, "task10_change_password").client
    h = bearer(c, "student@example.com", "password123")
    assert c.patch("/auth/me/password", json={"old_password": "nope", "new_password": "newpass123"}, headers=h).status_code == 400
    assert c.patch("/auth/me/password", json={"old_password": "password123", "new_password": "newpass123"}, headers=h).status_code == 200
    assert login(c, "student@example.com", "newpass123").status_code == 200


def test_solution_11_to_14(example, capsys):
    c = solution(example, "task11_cors").client
    assert c.get("/auth/me", headers={"Origin": "http://localhost:5173"}).headers["access-control-allow-origin"] == "http://localhost:5173"
    assert "access-control-allow-origin" not in c.get("/auth/me", headers={"Origin": "http://evil.example"}).headers

    c = solution(example, "task12_logging_middleware").client
    assert "X-Process-Time-ms" in c.get("/hello").headers
    assert c.get("/fail").status_code == 404
    assert "GET /fail -> 404" in capsys.readouterr().out

    ex = solution(example, "task13_welcome_email")
    ex.main.EMAIL_DELAY_SECONDS = 0
    assert register(ex.client).status_code == 201 and ex.main.SENT_EMAILS == ["ada@example.com"]
    assert register(ex.client).status_code == 409

    env = {"ADMIN_EMAIL": "boss@example.com", "ADMIN_PASSWORD": "boss123456"}
    c = solution(example, "task14_lifespan", env=env).client
    assert login(c, "boss@example.com", "boss123456").status_code == 200
    assert login(c, "boss@example.com", "wrong").status_code == 401
