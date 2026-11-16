# 14: Lifespan

## What is this?
A `lifespan` async context manager runs code **once at startup** (before `yield`) and **once at shutdown** (after). Here startup creates the tables and the first admin from `ADMIN_EMAIL` / `ADMIN_PASSWORD` in `.env`, **only if no admin exists yet**. This is the proper replacement for the module-level `create_all()` used in examples 03–13.

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste the output as SECRET_KEY in .env
```

`.env.example` already contains `ADMIN_EMAIL=admin@example.com` and `ADMIN_PASSWORD=admin12345`.

## Run it
```bash
cd 14_lifespan
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. **Authorize button:** click **Authorize** (top right, padlock icon). Type your **email** in `username`, your password in `password`, leave `client_id` / `client_secret` empty, and click **Authorize**, then **Close**. Swagger calls `POST /auth/login` for you and sends `Authorization: Bearer <token>` on every request. Routes with a padlock need it. Log in as the admin from `.env` and call **GET /admin/users**.

## TRY IT
1. Start → terminal: `[lifespan] STARTUP` + `created first admin: admin@example.com`
2. Restart → `an admin already exists: nothing to do`
3. Log in as `admin@example.com` / `admin12345` → `GET /auth/me` shows `role: admin`; `GET /admin/users` → 200
4. Ctrl+C → `[lifespan] SHUTDOWN`
5. ❌ register `ana@example.com` / `anapass123`, then `GET /admin/users` as ana → 403
6. ❌ `GET /admin/users` without a token → 401 · registering `admin@example.com` → 409

All requests are also in [`../test_requests.http`](../test_requests.http).
