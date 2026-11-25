# 09: Production Settings

## What it shows
- `config.py`: `secret_key` (required), `environment` (default `"development"`), `allowed_origins: list[str]`, and an `is_production` property.
- `main.py`: `docs_url`, `redoc_url` and `openapi_url` are `None` in production, and CORS uses `settings.allowed_origins`.
- **List values in env vars are JSON:** `ALLOWED_ORIGINS=["https://myapp.com","https://www.myapp.com"]`.
- `test_settings.py` re-imports the app with different environment variables.

### `fastapi dev` vs `fastapi run` vs `--workers`
| Command | Use it for | Reload on save | Listens on | Processes |
|---|---|---|---|---|
| `fastapi dev main.py` | development | ✅ yes | `127.0.0.1` (only your machine) | 1 |
| `fastapi run main.py` | production / Docker | ❌ no | `0.0.0.0` (reachable from outside) | 1 |
| `fastapi run main.py --workers 4` | production on a multi-core server | ❌ no | `0.0.0.0` | 4 separate processes (no shared memory! see 10) |

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste as SECRET_KEY in .env
```

To try production mode locally:
```bash
cp .env.production.example .env      # ENVIRONMENT=production
```

## Run
```bash
cd 09_production_settings
fastapi dev main.py          # development: /docs works
fastapi run main.py          # production-style server (with .env.production.example copied to .env)
pytest -v
```

## Expected output
Development: `GET /config` → `{"environment": "development", "allowed_origins": ["http://localhost:5173", "http://localhost:3000"], "docs_enabled": true}`, and `/docs` opens.
Production: `GET /config` → `{"environment": "production", "allowed_origins": ["https://myapp.com"], "docs_enabled": false}`, and `/docs` → **404**.
Without `SECRET_KEY`: the app refuses to start (`ValidationError ... secret_key Field required`).
Tests: `4 passed`.
