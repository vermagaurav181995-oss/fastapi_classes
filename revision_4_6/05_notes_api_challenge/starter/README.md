# 05: Notes API Challenge (starter)

Build a small, secure notes API using everything from Class 4 and Class 6. All data lives in Python dicts, with no database.

## What you get
Every file already exists with the right names and signatures; each body is `raise NotImplementedError`.
The app **starts** and `/docs` lists every route, but calling a route gives a 500 until you implement it.

| File | Implement |
|---|---|
| `config.py` | done: `Settings` with a required `secret_key` |
| `storage.py` | `find_user_by_email`, `add_user`, `add_note` |
| `schemas.py` | fields for `UserCreate`, `UserOut`, `Token`, `NoteCreate`, `NoteUpdate`, `NoteOut` |
| `security.py` | hashing, `create_access_token`, `get_current_user` |
| `exceptions.py` | `NoteNotFound` and `register_exception_handlers` |
| `routers/auth.py` | register, login, me |
| `routers/notes.py` | `Pagination`, ownership helpers, the five note routes, and protect the router |
| `main.py` | call `register_exception_handlers`, add CORS, register `log_requests` as middleware, `seed_admin` in `lifespan` |

## The spec

| Method | Path | Who | Success | Errors |
|---|---|---|---|---|
| POST | `/auth/register` | anyone | 201 `{id, email, role}` (no password!) | 409 duplicate email, 422 |
| POST | `/auth/login` | anyone (form: `username` = email) | 200 `{access_token, token_type: "bearer"}` | 401 (same message for wrong email or password) |
| GET | `/auth/me` | logged in | 200 `{id, email, role}` | 401 |
| POST | `/notes` | logged in | 201 note, `owner_id` = current user | 401, 422 |
| GET | `/notes?q=&skip=&limit=` | logged in | 200 **only my** notes; `q` searches title + content (`min_length=2`); `skip`/`limit` via a `Pagination` class dependency | 401, 422 |
| GET | `/notes/{id}` | owner | 200 | 404 missing, 403 not mine |
| PATCH | `/notes/{id}` | owner | 200, only the sent fields change (`exclude_unset`) | 404, 403, 422 |
| DELETE | `/notes/{id}` | owner **or admin** | 204 | 404, 403 |

**Also required**
- `NoteNotFound` exception + handler → 404 `{"error": "NoteNotFound", "message": "Note 7 does not exist"}`
- the notes router protected as a whole: `APIRouter(..., dependencies=[Depends(get_current_user)])`
- logging middleware: prints `METHOD path -> status (ms)` and adds an `X-Process-Time-ms` header
- CORS for `http://localhost:5173`
- passwords hashed with pwdlib; JWT with `"sub"` = user id as a string, plus `"exp"`; `SECRET_KEY` from `.env`
- all data in the dicts in `storage.py`

**Bonus**
- a `BackgroundTasks` job that prints `note <id> created by <email>` after `POST /notes`
- a `lifespan` that creates an admin from `ADMIN_EMAIL` / `ADMIN_PASSWORD` in `.env` if none exists

## Setup & run
```bash
cd 05_notes_api_challenge/starter
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste as SECRET_KEY in .env
fastapi dev main.py
```
Open http://127.0.0.1:8000/docs. Once login works, use **Authorize** (email in `username`).

## Check your work
Run the same scenario as the solution's README: two users, each sees only their own notes, 403 on the other's note, and the admin can delete any note.
The solution is in `../solution/`.
