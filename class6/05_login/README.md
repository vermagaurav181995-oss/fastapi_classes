# 05: Login

## What is this?
`POST /auth/login` uses **OAuth2PasswordRequestForm**: a *form* body with `username` (= the email) and `password`. It returns `{"access_token": ..., "token_type": "bearer"}`. A wrong email and a wrong password get the **same 401 message**, with a `WWW-Authenticate: Bearer` header, so attackers can't find out which emails exist.

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste the output as SECRET_KEY in .env
```

## Run it
```bash
cd 05_login
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. Register first, then **POST /auth/login** (it shows form fields, not JSON). **Authorize button:** click **Authorize** (top right, padlock icon). Type your **email** in `username`, your password in `password`, leave `client_id` / `client_secret` empty, and click **Authorize**, then **Close**. Swagger calls `POST /auth/login` for you and sends `Authorization: Bearer <token>` on every request. Routes with a padlock need it.

## TRY IT
1. `POST /auth/register` `{"email": "ada@example.com", "password": "supersecret"}` → 201
2. `POST /auth/login` form `username=ada@example.com&password=supersecret` → 200 `{access_token, token_type: "bearer"}`
3. ❌ wrong password → 401 `Incorrect email or password`
4. ❌ unknown email → 401 with the **same** message
5. ❌ JSON body instead of a form → 422

All requests are also in [`../test_requests.http`](../test_requests.http).
