# Class 6: Authentication, Security & Middleware

Runnable FastAPI examples. Each numbered folder is a **standalone app**.
Libraries: **pyjwt** (tokens), **pwdlib[argon2]** (password hashing), **pydantic-settings** (`.env`), **SQLAlchemy 2.0** + SQLite.

## Setup (once)

Requires **Python 3.11+**.

```bash
cd class6
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Secret key
Most examples need a `.env` file. In the example folder:
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"
```
Paste the printed value as `SECRET_KEY=...` in `.env`. **Never commit `.env`** (the `.gitignore` here already ignores `.env` and `*.db`).

## Running an example
```bash
cd 06_get_current_user_me
cp .env.example .env        # first time only, then set SECRET_KEY
fastapi dev main.py
```
Open http://127.0.0.1:8000/docs and use the **Authorize** button: enter your **email** as `username` plus your password. Stop with `Ctrl+C` before starting the next example (they all use port 8000). Each example creates its own `.db` file on startup; delete it to reset the data.

| # | Topic | .env? | Run (from `class6/`) |
|---|---|---|---|
| 01 | Password hashing with pwdlib | no | `cd 01_password_hashing && fastapi dev main.py` |
| 02 | Settings & required SECRET_KEY | yes | `cd 02_settings_secret_key && fastapi dev main.py` |
| 03 | User model + register (201/409/422) | yes | `cd 03_user_model_register && fastapi dev main.py` |
| 04 | Create / decode / tamper / expire JWTs | yes | `cd 04_jwt_create_decode && fastapi dev main.py` |
| 05 | Login with OAuth2PasswordRequestForm | yes | `cd 05_login && fastapi dev main.py` |
| 06 | `get_current_user`, `CurrentUser`, `/auth/me` | yes | `cd 06_get_current_user_me && fastapi dev main.py` |
| 07 | Protect a whole router | yes | `cd 07_protect_router && fastapi dev main.py` |
| 08 | Roles: `require_role()`, admin-only delete | yes | `cd 08_roles_require_role && fastapi dev main.py` |
| 09 | Ownership checks on reviews | yes | `cd 09_ownership_check && fastapi dev main.py` |
| 10 | Change password | yes | `cd 10_change_password && fastapi dev main.py` |
| 11 | CORS + tiny HTML frontend | yes | `cd 11_cors && fastapi dev main.py` (+ `cd frontend && python -m http.server 5173`) |
| 12 | Custom middleware (timing, request ID) | no | `cd 12_custom_middleware && fastapi dev main.py` |
| 13 | Background tasks (welcome email) | yes | `cd 13_background_tasks && fastapi dev main.py` |
| 14 | Lifespan: tables + first admin | yes | `cd 14_lifespan && fastapi dev main.py` |
| 15 | Full Bookstore API | yes | `cd 15_bookstore_full && fastapi dev main.py` |
| P | Practice tasks | yes (`practice/.env`) | `cd practice && fastapi dev task01_secret_key.py` |

## Other files
- `test_requests.http`: every request for the VS Code **REST Client** extension. Log in once per section and the token is reused through variables.
- `practice/`: 14 starter tasks with TODOs; answers in `practice/solutions/`.
- `test_all_examples.py`: automated tests for every example and solution (no `.env` needed):
  ```bash
  pytest -v test_all_examples.py
  ```
