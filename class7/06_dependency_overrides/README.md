# 06: Dependency Overrides

## What it shows
The app is the **in-memory bookstore with auth** from Class 6 (`config.py`, `storage.py`, `security.py`, `emails.py`, `routers/`, `main.py`). A lifespan seeds the admin `admin@example.com` / `admin12345` from `ADMIN_EMAIL` / `ADMIN_PASSWORD`.
`conftest.py` sets `SECRET_KEY` (≥ 32 characters), `ADMIN_EMAIL` and `ADMIN_PASSWORD` with `os.environ` **before** importing the app, because `config.py` reads them at import time.

`app.dependency_overrides[real] = fake` replaces a dependency **everywhere**, including inside dependency chains:
- `as_admin` / `as_user` fixtures override `get_current_user`, then **clear** the overrides after `yield`.
- `require_role("admin")` depends on `get_current_user`, so the fake user flows through the chain: fake admin → 204, fake user → 403, **with no token at all**.
- `fake_sender` overrides `get_email_sender` with a `FakeEmailSender` that records emails, so register's background task uses it.
- `test_without_override_the_real_check_is_back` proves the cleanup works (401 again).

## Setup
No `.env` needed for the tests.

## Run
```bash
cd 06_dependency_overrides
pytest -v
```

## Expected output
```
8 passed
```
