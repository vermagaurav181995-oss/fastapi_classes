# 09: Ownership Checks

## What is this?
Roles say what *kind* of user you are; ownership says whether *this* item is yours. Each `Review` has an `owner_id`, taken from the token and never from the body. `get_review_for_change()` allows the **owner** or an **admin**, and returns **403** for everyone else.

**Demo users (created on startup):**

| Email | Password | Role | Owns |
|---|---|---|---|
| admin@example.com | admin12345 | admin | none |
| alice@example.com | alice12345 | user | review 1 |
| bob@example.com | bob1234567 | user | review 2 |

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste the output as SECRET_KEY in .env
```

## Run it
```bash
cd 09_ownership_check
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. **Authorize button:** click **Authorize** (top right, padlock icon). Type your **email** in `username`, your password in `password`, leave `client_id` / `client_secret` empty, and click **Authorize**, then **Close**. Swagger calls `POST /auth/login` for you and sends `Authorization: Bearer <token>` on every request. Routes with a padlock need it. Log in as alice and PATCH review 1 (yours) and review 2 (bob's).

## TRY IT
1. `GET /reviews` → 200
2. `PATCH /reviews/1` `{"rating": 3}` as alice → 200
3. `PATCH /reviews/2` `{"text": "Edited by admin"}` as admin → 200
4. `DELETE /reviews/1` as alice → 204
5. ❌ `PATCH /reviews/2` or `DELETE /reviews/2` as alice → 403 `You can only change your own reviews`
6. ❌ no token → 401 · `rating: 9` → 422

All requests are also in [`../test_requests.http`](../test_requests.http).
