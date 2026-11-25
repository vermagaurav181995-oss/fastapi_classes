import importlib
import sys

from fastapi.testclient import TestClient
from storage import USERS


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_timing_header(client):
    assert "X-Process-Time-ms" in client.get("/health").headers


def test_cors_allowed_and_blocked(client):
    allowed = client.get("/health", headers={"Origin": "http://localhost:5173"})
    blocked = client.get("/health", headers={"Origin": "http://evil.com"})
    assert allowed.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert "access-control-allow-origin" not in blocked.headers


def test_admin_seeded_only_once(client):
    from main import seed_admin

    seed_admin()
    assert sum(user["role"] == "admin" for user in USERS.values()) == 1


def test_deleted_user_token_is_rejected(client, ana_headers):
    USERS.pop(2)
    assert client.get("/auth/me", headers=ana_headers).status_code == 401


def test_docs_hidden_in_production(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    saved = {name: sys.modules.pop(name) for name in ("config", "main") if name in sys.modules}
    try:
        app = importlib.import_module("main").app
        assert TestClient(app).get("/docs").status_code == 404
    finally:
        sys.modules.update(saved)
