# 01: Password Hashing (pwdlib + Argon2)

## What is this?
Never store plain passwords. `PasswordHash.recommended()` (Argon2id) turns a password into a slow, salted, one-way hash. `hash_password()` is used at register, `verify_password()` at login. Because of the random **salt**, hashing the same password twice gives two different strings, and both still verify.

## Setup
No `.env` needed for this example.

## Run it
```bash
cd 01_password_hashing
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. Try **GET /demo/hash** twice: different hashes every time. Then **GET /demo/verify** with a right and a wrong `attempt`.

## TRY IT
1. `GET /demo/hash?password=secret123` → 200, `hashes_are_equal: false`, `both_verify: true`
2. `GET /demo/verify?password=secret123&attempt=secret123` → 200 `is_valid: true`
3. `GET /demo/verify?password=secret123&attempt=wrong` → 200 `is_valid: false`
4. ❌ `GET /demo/hash?password=` → 422

All requests are also in [`../test_requests.http`](../test_requests.http).
