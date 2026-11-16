# 08: Roles with require_role()

## What is this?
`require_role(*roles)` is a **dependency factory**: a function that *returns* a dependency. `AdminUser = Annotated[User, Depends(require_role("admin"))]`. **401** = no or bad token (who are you?), **403** = valid token but wrong role (not allowed).

**Demo users (created on startup):**

| Email | Password | Role |
|---|---|---|
| admin@example.com | admin12345 | admin |
| user@example.com | user12345 | user |

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste the output as SECRET_KEY in .env
```

## Run it
```bash
cd 08_roles_require_role
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. **Authorize button:** click **Authorize** (top right, padlock icon). Type your **email** in `username`, your password in `password`, leave `client_id` / `client_secret` empty, and click **Authorize**, then **Close**. Swagger calls `POST /auth/login` for you and sends `Authorization: Bearer <token>` on every request. Routes with a padlock need it. Log in as **user@example.com** and try **DELETE /books/{book_id}** (403). Then click Logout, log in as **admin@example.com** and try again (204).

## TRY IT
1. `GET /books` → 200 (public)
2. `POST /books` `{"title": "Emma"}` as user → 201
3. `DELETE /books/1` as admin → 204
4. ❌ `DELETE /books/2` as user → 403 `Not enough permissions`
5. ❌ `DELETE /books/2` without a token → 401 · `DELETE /books/999` as admin → 404

All requests are also in [`../test_requests.http`](../test_requests.http).
