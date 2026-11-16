# Class 6: Practice Tasks

Each `taskNN_*.py` is a **starter**: it runs, but the TODOs aren't done. Fill them in, then compare with `solutions/`.
`common.py` contains the finished building blocks from class (settings, DB, `User`, hashing, tokens, `CurrentUser`, a ready-made `POST /auth/login`, and `seed_demo_users()`).

## Setup
```bash
cd practice
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste as SECRET_KEY in .env
fastapi dev task01_secret_key.py      # every task runs the same way
```
Solutions read the same `practice/.env`: `cd solutions && fastapi dev task01_secret_key.py`

Demo users (tasks 5–11): `student@example.com` / `password123` (user), `admin@example.com` / `admin12345` (admin).
All tasks share `practice.db`. Delete it to start fresh.

| # | Task | File | Example |
|---|---|---|---|
| 1 | SECRET_KEY in .env; app refuses to start without it | `task01_secret_key.py` | 02 |
| 2 | Create the User model | `task02_user_model.py` | 03 |
| 3 | `hash_password` / `verify_password`; hash twice and print | `task03_hashing.py` | 01 |
| 4 | `POST /auth/register`, 409 duplicate, no hash in response | `task04_register.py` | 03 |
| 5 | `POST /auth/login`; decode and print the payload | `task05_login.py` | 04, 05 |
| 6 | `GET /auth/me` with your own `CurrentUser` | `task06_me.py` | 06 |
| 7 | 1-minute expiry; `/me` returns 401 afterwards | `task07_token_expiry.py` | 06 |
| 8 | Protect the whole books router | `task08_protect_router.py` | 07 |
| 9 | `require_role`: admin-only DELETE (403 vs 204) | `task09_require_role.py` | 08 |
| 10 | `PATCH /auth/me/password` with the old password | `task10_change_password.py` | 10 |
| 11 | CORS for `http://localhost:5173` | `task11_cors.py` | 11 |
| 12 | Logging middleware: method, path, status, time | `task12_logging_middleware.py` | 12 |
| 13 | Welcome email with BackgroundTasks after register | `task13_welcome_email.py` | 13 |
| 14 | lifespan creates the first admin from `.env` | `task14_lifespan.py` | 14 |

Task 14 only creates its admin (`ADMIN_EMAIL`, default `boss@example.com`) if no admin exists yet. If you've already run tasks 5–11 (which seed `admin@example.com`), delete `practice.db` first.
