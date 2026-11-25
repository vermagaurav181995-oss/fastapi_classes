# <Project name>

> **TODO:** one or two sentences: what does this API do, and for whom?
> Note: data is stored in memory (Python dicts) and resets when the server restarts.

**Live URL:** https://<your-app>.onrender.com · **Health:** `/health`

## Features
- TODO: list the features (auth with JWT, ownership, admin role, filters, pagination, ...)

## Endpoints

| Method | Path | Access | Success | Errors |
|---|---|---|---|---|
| GET | `/health` | public | 200 | |
| POST | `/auth/register` | public | 201 | 409, 422 |
| POST | `/auth/login` | public | 200 token | 401 |
| GET | `/auth/me` | user | 200 | 401 |
| GET | `/items` | user (own items) | 200 | 401 |
| POST | `/items` | user | 201 | 401, 422 |
| GET | `/items/{item_id}` | owner / admin | 200 | 401, 403, 404 |
| PATCH | `/items/{item_id}` | owner | 200 | 401, 403, 404, 422 |
| DELETE | `/items/{item_id}` | owner / admin | 204 | 401, 403, 404 |
| TODO | `/admin/...` | **admin** | | 401, 403 |

## Setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste as SECRET_KEY in .env
```

## Run
```bash
fastapi dev main.py          # http://127.0.0.1:8000/docs
```
Admin for testing: `ADMIN_EMAIL` / `ADMIN_PASSWORD` from `.env` (default `admin@example.com` / `admin12345`).

## Tests
```bash
pytest -v
pytest --cov=. --cov-report=term-missing
```
TODO: paste your coverage table here.

## Docker
```bash
docker build -t my-capstone .
docker run --rm --env-file .env -p 8000:8000 my-capstone
```

## Deploy (Render)
Push to GitHub → Render **New + → Blueprint** (uses `render.yaml`) or **Web Service** with:
build `pip install -r requirements.txt`, start `fastapi run main.py --port $PORT`, env vars `SECRET_KEY` (generate), `ENVIRONMENT=production`, `ALLOWED_ORIGINS`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`.

---

### How to use this template (delete this section in your project)
1. Copy the folder: `cp -r 14_capstone/template ~/my-capstone && cd ~/my-capstone && git init`
2. Rename `items` to your resource (`tasks`, `posts`, `expenses`...) in `storage.py`, `schemas.py`, `routers/items.py` and `main.py`.
3. Implement every `TODO` in `routers/items.py` (each route currently answers **501 Not Implemented**).
4. Delete `test_items_are_not_implemented_yet` in `tests/test_app.py` and write `tests/test_items.py`.
5. Already done for you: `config.py`, `security.py` (hashing, tokens, `get_current_user`, `require_role`), `routers/auth.py`, `dependencies.py` (`Pagination`), `exceptions.py` (`NotFoundError`), `main.py` (lifespan, CORS, timing middleware, `/health`, docs hidden in production), the tests in `tests/` (13 passing), `Dockerfile`, `.dockerignore`, `.gitignore`, `render.yaml`.
