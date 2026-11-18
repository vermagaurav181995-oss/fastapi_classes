# Revision Quiz: Answers

**1.** Without `Query()`, FastAPI treats a `list` parameter as part of the **request body**, so `?tag=a&tag=b` is ignored. Fix:
```python
def filter_items(tag: Annotated[list[str] | None, Query()] = None): ...
```

**2.**
a) **422**, from FastAPI: `0` fails `ge=1`.
b) **422**, from FastAPI: `"abc"` is not an int.
c) **404**, from **your code** (`raise HTTPException(404)` or a custom exception): the input is valid, but the item doesn't exist.

**3.** `{"name": None, "price": 2}`. `model_dump()` includes every field, and the unsent ones are `None`. Fix: `changes.model_dump(exclude_unset=True)` returns only the fields the client actually sent → `{"name": "Pen", "price": 2}`.

**4.** A `field_validator` only sees **one** field's value (and fields are validated one by one, so `confirm_password` may not be available yet). `model_validator(mode="after")` runs after **all** fields are validated, on the finished model, so it can compare `self.password` with `self.confirm_password`.

**5.** `Depends(pagination)` passes the **function**: FastAPI calls it on every request and fills `skip`/`limit` from the query string (with validation). `Depends(pagination())` calls it **yourself, once, at import time**, and hands FastAPI the result (a dict). FastAPI needs a callable, so the app crashes on startup with `TypeError: ... is not a callable object`. Even without `Depends` (`page: dict = pagination()`), the query params are silently ignored.

**6.** Not reliably: when the route raises, the exception is thrown back into the generator **at the `yield`**, so the line after it never runs. Use `try / finally`:
```python
def get_connection():
    connection = open_connection()
    try:
        yield connection
    finally:
        connection.close()
```

**7.** Each hash string contains the **algorithm, its settings and a random salt**, e.g. `$argon2id$v=19$m=65536,t=3,p=4$<salt>$<hash>`. `verify` reads the salt from the stored string, hashes the attempt with it, and compares. Random salts mean two users with the same password get different hashes, and precomputed "rainbow tables" are useless.

**8.**
a) **Yes.** The payload is only base64url-encoded, not encrypted. Never put secrets in it.
b) **No.** The signature is computed over the header and payload with `SECRET_KEY`. Changing `sub` invalidates the signature, `jwt.decode` raises `InvalidSignatureError` and the API answers 401. Only someone with the secret key can sign a new token (which is why it must never be in your code or on GitHub).
c) The JWT spec (and PyJWT ≥ 2.10) requires `sub` to be a **string**. Convert back with `int(payload["sub"])`.

**9.**
a) **401**: not authenticated.
b) **401**: the credentials are no longer valid.
c) **403**: we know who you are, but you're not allowed.
d) **403**: authenticated, but not the owner. (Some APIs return 404 here to hide that the note exists.)

**10.**
a) **CORS:** `http://localhost:5173` isn't in `allow_origins`, so the response has no matching `Access-Control-Allow-Origin` header and the **browser** blocks it. CORS is enforced only by browsers on **cross-origin** requests: `/docs` is served from the API's own origin, and curl/Postman don't apply CORS at all.
b) **B.** The middleware registered **last** is the **outermost** layer, so it runs first on the way in (and last on the way out).
