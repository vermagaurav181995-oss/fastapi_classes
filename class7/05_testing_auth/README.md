# 05: Testing Auth

## What it shows
The app is the **in-memory bookstore with auth** from Class 6 (`config.py`, `storage.py`, `security.py`, `emails.py`, `routers/`, `main.py`). A lifespan seeds the admin `admin@example.com` / `admin12345` from `ADMIN_EMAIL` / `ADMIN_PASSWORD`.
`conftest.py` sets `SECRET_KEY` (≥ 32 characters), `ADMIN_EMAIL` and `ADMIN_PASSWORD` with `os.environ` **before** importing the app, because `config.py` reads them at import time.

| Fixture / helper (conftest.py) | Does |
|---|---|
| `reset_data` (autouse) | clears **books and users**, reseeds the books, cleans up after `yield` |
| `client` | `with TestClient(app)`, which runs the lifespan so the admin exists |
| `auth_headers(client, email, password)` | logs in, returns `{"Authorization": "Bearer ..."}` |
| `admin_headers`, `user_headers` | ready-made headers for the admin and for a registered user |

Tests: register + me, the hash never in the response, 409 duplicate, 422 short password, 401 wrong password (same message as for an unknown email), me with no token / fake token / **expired token** (`create_access_token(user_id, expires_minutes=-1)`), delete as nobody **401** / user **403** / admin **204**.

## Setup
No `.env` needed for the tests. To run the app: ```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste as SECRET_KEY in .env
```

## Run
```bash
cd 05_testing_auth
pytest -v
fastapi dev main.py     # the app itself (needs .env)
```

## Expected output
```
14 passed
```
