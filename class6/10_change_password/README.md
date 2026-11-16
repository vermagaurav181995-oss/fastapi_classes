# 10: Change Password

## What is this?
`PATCH /auth/me/password` needs a valid token **and** the old password (400 if it's wrong), so someone at an unlocked laptop can't take over the account. The new password must be at least 8 characters (422). Old tokens keep working until they expire, because JWTs are stateless.

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste the output as SECRET_KEY in .env
```

## Run it
```bash
cd 10_change_password
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. Register first. **Authorize button:** click **Authorize** (top right, padlock icon). Type your **email** in `username`, your password in `password`, leave `client_id` / `client_secret` empty, and click **Authorize**, then **Close**. Swagger calls `POST /auth/login` for you and sends `Authorization: Bearer <token>` on every request. Routes with a padlock need it. Call **PATCH /auth/me/password**, then log in again with the new password.

## TRY IT
1. Register `ada@example.com` / `supersecret`, log in
2. `PATCH /auth/me/password` `{"old_password": "supersecret", "new_password": "evenmoresecret"}` → 200
3. Log in with `evenmoresecret` → 200
4. ❌ log in with the old password → 401
5. ❌ wrong `old_password` → 400 `Old password is incorrect` · `new_password: "short"` → 422 · no token → 401

All requests are also in [`../test_requests.http`](../test_requests.http).
