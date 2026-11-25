import importlib
import sys

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

SECRET = "test-secret-key-that-is-at-least-32-characters-long"


def load_app(monkeypatch, **env):
    for key in ("SECRET_KEY", "ENVIRONMENT", "ALLOWED_ORIGINS"):
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    for module in ("main", "config"):
        sys.modules.pop(module, None)
    return importlib.import_module("main").app


def test_development_shows_docs(monkeypatch):
    app = load_app(monkeypatch, SECRET_KEY=SECRET, ENVIRONMENT="development")
    client = TestClient(app)
    assert client.get("/docs").status_code == 200
    assert client.get("/config").json()["docs_enabled"] is True


def test_production_hides_docs(monkeypatch):
    app = load_app(monkeypatch, SECRET_KEY=SECRET, ENVIRONMENT="production", ALLOWED_ORIGINS='["https://myapp.com"]')
    client = TestClient(app)
    assert client.get("/docs").status_code == 404
    assert client.get("/openapi.json").status_code == 404
    assert client.get("/config").json() == {
        "environment": "production",
        "allowed_origins": ["https://myapp.com"],
        "docs_enabled": False,
    }


def test_cors_uses_allowed_origins(monkeypatch):
    app = load_app(monkeypatch, SECRET_KEY=SECRET, ENVIRONMENT="production", ALLOWED_ORIGINS='["https://myapp.com"]')
    client = TestClient(app)
    allowed = client.get("/", headers={"Origin": "https://myapp.com"})
    blocked = client.get("/", headers={"Origin": "http://localhost:5173"})
    assert allowed.headers["access-control-allow-origin"] == "https://myapp.com"
    assert "access-control-allow-origin" not in blocked.headers


def test_missing_secret_key_refuses_to_start(monkeypatch):
    for key in ("SECRET_KEY", "ENVIRONMENT", "ALLOWED_ORIGINS"):
        monkeypatch.delenv(key, raising=False)
    sys.modules.pop("config", None)
    with pytest.raises(ValidationError, match="secret_key"):
        config = importlib.import_module("config")
        config.Settings(_env_file=None)
