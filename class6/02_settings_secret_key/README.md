# 02: Settings & the SECRET_KEY

## What is this?
Secrets live in `.env` (ignored by git), not in code. `config.py` uses **pydantic-settings**: `SECRET_KEY` has **no default**, so the app refuses to start without it. Other settings have defaults that `.env` can override.

**What happens without SECRET_KEY** (delete the line from `.env`, then start):
```
pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings
secret_key
  Field required [type=missing, input_value={...}, input_type=dict]
```

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste the output as SECRET_KEY in .env
```

## Run it
```bash
cd 02_settings_secret_key
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. Call **GET /settings**. Note that it shows the key's *length*, never the key.

## TRY IT
1. `GET /settings` → 200 `{"algorithm": "HS256", "access_token_expire_minutes": 30, ...}`
2. Change `ACCESS_TOKEN_EXPIRE_MINUTES=5` in `.env`: the server reloads and `/settings` shows 5
3. ❌ `GET /settings/secret_key` → 404
4. ❌ remove `SECRET_KEY` from `.env` → the server does not start (error above)

All requests are also in [`../test_requests.http`](../test_requests.http).
