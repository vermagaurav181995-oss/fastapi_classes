# 05: Notes API Challenge (solution)

A full implementation of the challenge spec: register/login with pwdlib + JWT, a protected notes router, ownership checks, a `Pagination` class dependency, a `NoteNotFound` handler, logging middleware, CORS, a background "note created" job and a lifespan that seeds an admin.

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
cd 05_notes_api_challenge/solution
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste as SECRET_KEY in .env
fastapi dev main.py
```
Admin from `.env`: `admin@example.com` / `admin12345`.

## Open in /docs
http://127.0.0.1:8000/docs. Click **Authorize**, put your **email** in `username` plus your password, and click **Authorize**. To switch users, click **Logout** in the same dialog and log in again.

## TRY IT
1. `POST /auth/register` `{"email": "ana@example.com", "password": "anapass123"}` → 201
2. `POST /auth/register` `{"email": "ben@example.com", "password": "benpass123"}` → 201
3. Log in as ana → `POST /notes` `{"title": "Shopping", "content": "milk, eggs"}` → 201 `{"id": 1, ..., "owner_id": 2}`; the terminal prints `[background] note 1 created by ana@example.com`
4. Log in as ben → `POST /notes` `{"title": "Ben ideas", "content": "start a band"}` → 201 (`id` 2)
5. As ana: `GET /notes` → only note 1 · `GET /notes?q=milk` → note 1 · `GET /notes?limit=1&skip=1` → `[]`
6. As ana: `PATCH /notes/1` `{"content": "milk, eggs, bread"}` → 200, title unchanged
7. As admin: `DELETE /notes/2` → 204 (admins may delete any note)
8. ❌ As ana: `GET /notes/2` (before step 7) → 403 `This note belongs to someone else`
9. ❌ As ben: `PATCH /notes/1` → 403 · `DELETE /notes/1` → 403
10. ❌ `GET /notes` without a token → 401 `Not authenticated`
11. ❌ `GET /notes/99` → 404 `{"error": "NoteNotFound", "message": "Note 99 does not exist"}`
12. ❌ `GET /notes?q=a` → 422 (q needs 2+ characters)
13. ❌ register ana again → 409 · password `short` → 422 · wrong password at login → 401
