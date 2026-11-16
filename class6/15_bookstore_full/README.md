# 15: Bookstore API (full project)

## What is this?
Everything from Class 6 in one project:

| File | What's inside |
|---|---|
| `config.py` | pydantic-settings, required `SECRET_KEY`, first-admin settings |
| `database.py` | engine, `SessionLocal`, `get_db`, `DbSession` |
| `models.py` | `User`, `Author`, `Book`, `Review` (cascade deletes) |
| `schemas.py` | Create / Update / Out schemas; no password ever goes out |
| `security.py` | pwdlib hashing, PyJWT tokens, `get_current_user`, `CurrentUser`, `require_role`, `AdminUser` |
| `exceptions.py` | `NotFoundError` → 404, `ConflictError` → 409, JSON `{"error", "message"}` |
| `routers/auth.py` | register (+ background welcome email), login, me, change password |
| `routers/authors.py` `routers/books.py` `routers/reviews.py` | public reads, user writes, admin deletes, owner-only review edits |
| `main.py` | lifespan (tables + first admin + sample books), CORS, logging middleware (`X-Process-Time-ms`), exception handlers |

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste the output as SECRET_KEY in .env
```
`.env.example` sets the first admin to `admin@example.com` / `admin12345`.

## Run it
```bash
cd 15_bookstore_full
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. Click **Authorize**, put your **email** in `username` and your password in `password`, and click **Authorize**. All padlocked routes now send your token. To switch between a normal user and the admin, click **Logout** in the same dialog and log in again.

## Endpoints

| Method | Path | Who | Success | Errors |
|---|---|---|---|---|
| GET | `/` | public | 200 | |
| POST | `/auth/register` | public | 201 `UserOut` (+ background email) | 409, 422 |
| POST | `/auth/login` | public | 200 `{access_token, token_type}` | 401 |
| GET | `/auth/me` | user | 200 `UserOut` | 401 |
| PATCH | `/auth/me/password` | user | 200 | 400 wrong old password, 401, 422 |
| GET | `/authors` | public | 200 `list[AuthorOut]` | |
| GET | `/authors/{author_id}` | public | 200 | 404 |
| GET | `/authors/{author_id}/books` | public | 200 `list[BookOut]` | 404 |
| POST | `/authors` | user | 201 | 401, 409 duplicate name, 422 |
| DELETE | `/authors/{author_id}` | **admin** | 204 (also deletes their books) | 401, 403, 404 |
| GET | `/books?skip=&limit=&author_id=` | public | 200 `list[BookOut]` | 422 |
| GET | `/books/{book_id}` | public | 200 | 404 |
| POST | `/books` | user | 201 | 401, 404 unknown author, 422 |
| DELETE | `/books/{book_id}` | **admin** | 204 | 401, 403, 404 |
| GET | `/books/{book_id}/reviews` | public | 200 `list[ReviewOut]` | 404 |
| POST | `/books/{book_id}/reviews` | user | 201 | 401, 404, 422 |
| PATCH | `/reviews/{review_id}` | **owner or admin** | 200 | 401, 403, 404, 422 |
| DELETE | `/reviews/{review_id}` | **owner or admin** | 204 | 401, 403, 404 |

Every response also carries an `X-Process-Time-ms` header, and the terminal logs `METHOD path -> status (ms)`.
CORS allows `http://localhost:5173` and `http://localhost:3000`.

## TRY IT
1. `GET /books` → 200 `[Dune, 1984, Animal Farm]` (seeded on startup)
2. `POST /auth/register` `{"email": "ada@example.com", "password": "supersecret"}` → 201, and the terminal prints the welcome email
3. Log in as ada → `POST /books` `{"title": "Emma", "year": 1815, "author_id": 1}` → 201
4. `POST /books/1/reviews` `{"rating": 5, "text": "Great"}` → 201
5. Log in as `admin@example.com` / `admin12345` → `DELETE /books/3` → 204
6. ❌ register ada again → 409 `{"error": "Conflict", "message": "Email already registered"}`
7. ❌ `POST /books` without a token → 401
8. ❌ `DELETE /books/1` as ada → 403 `Not enough permissions`
9. ❌ `PATCH /reviews/<admin's review>` as ada → 403 `You can only change your own reviews`
10. ❌ `GET /books/999` → 404 `{"error": "NotFound", "message": "Book 999 not found"}`
11. ❌ `POST /books` `{"title": "", "author_id": 1}` → 422

All requests are also in [`../test_requests.http`](../test_requests.http).
