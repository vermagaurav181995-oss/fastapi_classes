# 03: Class 6 Recap

## What is this?
The Class 6 auth stack in one app, with users stored in a dict:

| Piece | Where |
|---|---|
| Settings from `.env` (required `SECRET_KEY`, first-admin credentials) | `config.py` |
| pwdlib hashing, JWT (`sub` + `exp`), `get_current_user`, `require_role`, `AdminUser` | `security.py` |
| `POST /auth/register` (+ background welcome email), `POST /auth/login`, `GET /auth/me` | `routers/auth.py` |
| Admin-only `GET /admin/users` and `GET /admin/emails` | `routers/admin.py` |
| Lifespan that seeds the admin from `.env`, CORS for `http://localhost:5173`, timing middleware | `main.py` |

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste the output as SECRET_KEY in .env
```
`.env.example` sets the admin to `admin@example.com` / `admin12345`.

## Run it
```bash
cd 03_class6_recap
fastapi dev main.py
```
The terminal shows `[lifespan] admin created: admin@example.com` on startup.

## Open in /docs
http://127.0.0.1:8000/docs. Click **Authorize** (top right), put your **email** in `username` and your password in `password`, leave `client_id` / `client_secret` empty, and click **Authorize**. Swagger calls `POST /auth/login` and sends `Authorization: Bearer <token>` on every padlocked route. To switch users, click **Logout** in the same dialog and log in again.

## TRY IT
1. `POST /auth/register` `{"email": "ana@example.com", "password": "anapass123"}` → 201 `{"id": 2, "email": "ana@example.com", "role": "user"}`; the terminal prints `[email] welcome email sent to ana@example.com`
2. `POST /auth/login` form `username=ana@example.com&password=anapass123` → 200 `{access_token, token_type: "bearer"}`
3. `GET /auth/me` + ana's token → 200 · every response has an `X-Process-Time-ms` header
4. Log in as admin → `GET /admin/users` → 200 (2 users) · `GET /admin/emails` → `["ana@example.com"]`
5. `GET /auth/me` with header `Origin: http://localhost:5173` → `access-control-allow-origin: http://localhost:5173`
6. ❌ register ana again → 409 `Email already registered` · password `short` → 422
7. ❌ login with the wrong password → 401 `Incorrect email or password`
8. ❌ `GET /auth/me` without a token / with an expired token → 401
9. ❌ `GET /admin/users` + ana's token → 403 `Not enough permissions`
10. ❌ `Origin: http://localhost:3000` → no `access-control-allow-origin` header

All requests are also in [`../test_requests.http`](../test_requests.http).
