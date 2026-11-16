# 03: User Model & Register

## What is this?
`models.py` defines the **User table** (id, unique email, hashed_password, role="user", is_active). `schemas.py` separates **UserCreate** (EmailStr + password ≥ 8 chars) from **UserOut** (no password field, so the hash can never leak). `POST /auth/register` returns **201**, **409** for a taken email and **422** for invalid input.

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste the output as SECRET_KEY in .env
```

## Run it
```bash
cd 03_user_model_register
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. Use **POST /auth/register**, then **GET /users**. Neither response contains a password.

## TRY IT
1. `POST /auth/register` `{"email": "ada@example.com", "password": "supersecret"}` → 201 `{"id": 1, "email": ..., "role": "user", "is_active": true}`
2. Open `users.db` in a SQLite viewer: `hashed_password` starts with `$argon2id$`
3. ❌ same request again → 409 `Email already registered`
4. ❌ password `short` → 422 · email `not-an-email` → 422

All requests are also in [`../test_requests.http`](../test_requests.http).
