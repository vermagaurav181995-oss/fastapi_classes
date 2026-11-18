# 01: The Request Journey

## What is this?
One app where a single request passes through **every** layer from Class 4 and Class 6, so you can watch the order in the terminal:

```
request
  → CORSMiddleware                  (adds Access-Control-* headers for http://localhost:5173)
  → log_and_time_requests           (prints "->", starts the timer)
  → router: DELETE /books/{book_id}
  → dependencies, in order:
       oauth2_scheme                 no "Authorization: Bearer" header?   → 401
       get_current_user              bad / expired token?                → 401
       require_role("admin")         not an admin?                       → 403
       get_book_store  (yield)       prints "[store] setup"
  → parameter validation             book_id must be >= 1 (Path(ge=1))   → 422
  → the route                        book missing → raise BookNotFound   → 404 (custom handler)
                                     else delete + queue a background job → 204
  → response leaves the middleware   (prints "<-" with status + time, adds X-Process-Time-ms)
  → background task                  prints "[background] deletion ... recorded"
  → yield cleanup                    prints "[store] cleanup"
```

| File | Contents |
|---|---|
| `main.py` | lifespan (seeds users), CORS, logging/timing middleware, exception handlers, routers |
| `security.py` | pwdlib hashing, JWT, `oauth2_scheme` → `get_current_user` → `require_role` |
| `routers/books.py` | `Path(ge=1)`, the `get_book_store` yield dependency, `BackgroundTasks` on delete |
| `routers/auth.py` | login and me |
| `exceptions.py` | `BookNotFound` + handler |
| `storage.py` | the dicts: `USERS`, `BOOKS`, `DELETION_LOG` |

**Users seeded on startup**

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
cd 01_request_journey
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. Click **Authorize** (top right), put your **email** in `username` and your password in `password`, leave `client_id` / `client_secret` empty, and click **Authorize**. Swagger calls `POST /auth/login` and sends `Authorization: Bearer <token>` on every padlocked route. To switch users, click **Logout** in the same dialog and log in again.

## Walkthrough: five requests to `DELETE /books/{book_id}`
Keep the terminal next to you. Lines are shortened.

**1. No token → 401**
`DELETE /books/1` without `Authorization`
```
[middleware] -> DELETE /books/1
[middleware] <- DELETE /books/1 401
```
`oauth2_scheme` finds no header and stops the request: `{"detail": "Not authenticated"}`. No other dependency runs, and neither does the route.

**2. `book_id=0` → 422** (as **admin**)
`DELETE /books/0` with the admin token
```
[middleware] -> DELETE /books/0
[store] setup: book store opened
[store] cleanup: book store closed
[middleware] <- DELETE /books/0 422
```
FastAPI runs the **dependencies first** and validates the parameters afterwards. The auth chain passes and the store opens, then `Path(ge=1)` rejects `0`, so the route never runs, but the yield cleanup still does.
Try the same request as the **normal user**: you get **403**, not 422, because `require_role` fails before validation happens.

**3. Normal user → 403**
`DELETE /books/1` with the user token
```
[middleware] -> DELETE /books/1
[middleware] <- DELETE /books/1 403
```
The token is valid (so not 401), but `require_role("admin")` says *not allowed*: `{"detail": "Not enough permissions"}`.

**4. Missing book → 404** (as admin)
`DELETE /books/99`
```
[store] setup: book store opened
[route] admin@example.com deletes book 99
[store] cleanup: book store closed
[middleware] <- DELETE /books/99 404
```
The route raises `BookNotFound(99)`, and the custom handler turns it into `{"error": "BookNotFound", "message": "Book 99 does not exist"}`. No background task was queued, because the route failed.

**5. Admin → 204**
`DELETE /books/1`
```
[middleware] -> DELETE /books/1
[store] setup: book store opened
[route] admin@example.com deletes book 1
[middleware] <- DELETE /books/1 204 (0.56 ms)
[background] deletion of 'Dune' recorded
[store] cleanup: book store closed
```
The response (empty body, `X-Process-Time-ms` header) is finished **before** the background task runs, and the yield cleanup runs last. `GET /books/admin/deletions` (admin) now returns `["Dune"]`.

## TRY IT
1. `GET /books` → 200 (public)
2. `GET /books/2` → 200 · `GET /books/0` → 422 · `GET /books/99` → 404 `BookNotFound`
3. Log in as admin and as user (form `username=...&password=...` on `POST /auth/login`)
4. `GET /auth/me` → 200 your user · ❌ without a token → 401
5. The five `DELETE` cases above: 401, 422, 403, 404, 204
6. `GET /books` with header `Origin: http://localhost:5173` → response has `access-control-allow-origin: http://localhost:5173`

All requests are also in [`../test_requests.http`](../test_requests.http).
