# 04: Creating & Decoding JWTs

## What is this?
A JWT is `header.payload.signature`. The payload (`{"sub": "<user id>", "exp": <timestamp>}`) is only base64, so **anyone can read it**. The signature uses `SECRET_KEY`, so **nobody can change it**. `jwt.decode()` checks the signature and the expiry.

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste the output as SECRET_KEY in .env
```

## Run it
```bash
cd 04_jwt_create_decode
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. Get a token from **GET /demo/token**, paste it into **GET /demo/decode**, and also paste it into https://jwt.io to see the readable payload. Then try **/demo/tampered** and **/demo/expired**.

## TRY IT
1. `GET /demo/token?user_id=7` → 200 `{"access_token": "eyJ...", "payload": {"sub": "7", "exp": ...}}`
2. `GET /demo/decode?token=<token>` → 200 `{"valid": true, ...}`
3. ❌ `GET /demo/tampered` → 401 `Invalid token: Signature verification failed`
4. ❌ `GET /demo/expired` → 401 `Token has expired`
5. ❌ `GET /demo/decode?token=abc` → 401 · `GET /demo/token?user_id=0` → 422

All requests are also in [`../test_requests.http`](../test_requests.http).
