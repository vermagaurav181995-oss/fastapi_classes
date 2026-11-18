# Spot the Bug: Answers

## Bug 01: tags filter
**Cause:** `tag: list[str] | None = None` has no `Query()`. FastAPI treats a `list` parameter without `Query()` as part of the **JSON body**, so `?tag=music` in the URL is ignored and `tag` is always `None`.
**Fix:** `tag: Annotated[list[str] | None, Query()] = None`
**Clue:** in `/docs`, the buggy route asks for `tag` in a *Request body* box.

## Bug 02: partial update
**Cause:** `changes.model_dump()` includes **every** field of `ItemUpdate`, and the ones the client didn't send are `None`. `item.update(...)` then overwrites the stored values with `None`.
**Fix:** `changes.model_dump(exclude_unset=True)` returns only the fields the client actually sent.

## Bug 03: dependency called instead of passed
**Cause:** the buggy code **calls** the dependency itself: `page: dict = pagination()`. That runs once at import time with the defaults, and `{"skip": 0, "limit": 5}` becomes a fixed default. FastAPI never sees `skip`/`limit` as query parameters, so they are ignored and never validated (`/docs` even shows `page` as a request body).
The same mistake inside `Depends` (`Depends(pagination())`) fails even earlier: the app crashes on startup with `TypeError: {'skip': 0, 'limit': 5} is not a callable object`.
**Fix:** pass the function, don't call it: `page: Annotated[dict[str, int], Depends(pagination)]`.

## Bug 04: connection cleanup
**Cause:** `get_connection()` uses `return`, so FastAPI has no place to run cleanup after the request, and `close()` is never called.
**Fix:** make it a **yield dependency** with `try / finally`:
```python
def get_connection():
    connection = FakeConnection()
    try:
        yield connection
    finally:
        connection.close()
```
The `finally` block runs after the response, even when the route raises an error.

## Bug 05: plain password
**Cause:** register stores `data.password` as-is. Anyone who reads the storage (a leak, a backup, a curious admin) can log in as every user, and also on other sites where they reused the password.
**Fix:** store `password_hash.hash(data.password)` (pwdlib, Argon2) in `hashed_password`, and check passwords with `password_hash.verify(plain, hashed)`. Argon2 is slow and salted, so a leaked hash can't be used to log in.

## Bug 06: login messages
**Cause:** an unknown email gets **404 "No account with this email"**, but a known email with the wrong password gets **401 "Wrong password"**. An attacker can try a list of emails and learn which ones are registered (*user enumeration*).
**Fix:** one check, one answer: `if user is None or not verify(...)` → **401 "Incorrect email or password"** (with `WWW-Authenticate: Bearer`).

## Bug 07: 401 instead of 403
**Cause:** the role check raises **401 Unauthorized** for a logged-in user who isn't an admin. 401 means "who are you? (missing/bad credentials)", so clients react by logging the user out or asking them to log in again.
**Fix:** use **403 Forbidden**: "I know who you are, but you're not allowed." Keep 401 only for a missing or invalid token.

## Bug 08: secret in code
**Cause:** `SECRET_KEY = "my-super-secret-jwt-key-do-not-share-2026"` is hard-coded in `security.py` and pushed to GitHub. Anyone can sign their own token: `jwt.encode({"sub": "1", "exp": ...}, "<that key>", algorithm="HS256")`, and the API trusts it.
**Fix:** load the key from the environment with pydantic-settings (`config.py`, `secret_key: str` with **no default**), keep it in a git-ignored `.env`, and commit only `.env.example`. If a key was ever pushed, **rotate it** (generate a new one), because it stays in the git history.

## Bug 09: CORS origin
**Cause:** `allow_origins=["http://localhost:3000"]`, but the frontend runs on `http://localhost:5173`. The browser sends `Origin: http://localhost:5173`, the response has no matching `Access-Control-Allow-Origin`, and the **browser** blocks it. curl, Postman and `/docs` don't enforce CORS, so they "work".
**Fix:** add the exact origin: `allow_origins=["http://localhost:3000", "http://localhost:5173"]`. Scheme, host and port must all match, and `localhost` ≠ `127.0.0.1`.
