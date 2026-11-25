# Task Manager API (capstone reference solution)

Users create **projects** and add **tasks** to them. Tasks have a status (`todo` / `in_progress` / `done`) and an optional due date.
Users only see and change their own data; **admins** can read and delete everything and see stats.
Data is stored in memory (Python dicts) and resets when the server restarts.

## Endpoints

| Method | Path | Access | Success | Errors |
|---|---|---|---|---|
| GET | `/health` | public | 200 `{"status": "ok"}` | |
| POST | `/auth/register` | public | 201 | 409 duplicate email, 422 |
| POST | `/auth/login` | public (form: `username` = email) | 200 token | 401 |
| GET | `/auth/me` | user | 200 | 401 |
| POST | `/projects` | user | 201 (owner = you) | 401, 422 |
| GET | `/projects?skip=&limit=` | user (own) · **admin: all** | 200 | 401, 422 |
| GET | `/projects/{id}` | owner · admin | 200 | 401, 403, 404 |
| PATCH | `/projects/{id}` | owner | 200 (only the sent fields change) | 401, 403, 404, 422 |
| DELETE | `/projects/{id}` | owner · admin | 204 (its tasks are deleted too) | 401, 403, 404 |
| POST | `/projects/{id}/tasks` | owner | 201 | 401, 403, 404, 422 |
| GET | `/projects/{id}/tasks` | owner · admin | 200 | 401, 403, 404 |
| GET | `/tasks?status=&due_before=&due_after=&project_id=&skip=&limit=` | user (own) · **admin: all** | 200, sorted by due date (no date last) | 401, 422 |
| GET | `/tasks/{id}` | owner · admin | 200 | 401, 403, 404 |
| PATCH | `/tasks/{id}` | owner | 200 | 401, 403, 404, 422 |
| DELETE | `/tasks/{id}` | owner · admin | 204 | 401, 403, 404 |
| GET | `/admin/users` | **admin** | 200 | 401, 403 |
| GET | `/admin/stats` | **admin** | 200 counts + tasks by status | 401, 403 |

Errors for missing things look like `{"error": "NotFound", "message": "Task 99 not found"}`.

## Structure
```
main.py           lifespan (seeds the admin), CORS, timing middleware, /health, docs hidden in production
config.py         settings (SECRET_KEY required, ENVIRONMENT, ALLOWED_ORIGINS, ADMIN_*)
security.py       pwdlib, JWT, get_current_user, require_role / AdminUser
permissions.py    ensure_owner(), get_project_or_404(), get_task_or_404()
dependencies.py   Pagination
exceptions.py     NotFoundError + handler
schemas.py        users, projects, tasks (TaskStatus enum, due_date: date)
storage.py        USERS / PROJECTS / TASKS dicts
routers/          auth, projects, tasks, admin
tests/            54 tests: auth, projects, tasks (parametrized filters), admin, app
```

## Setup & run
```bash
cd 14_capstone/example_task_manager
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste as SECRET_KEY in .env
fastapi dev main.py
```
Admin: `admin@example.com` / `admin12345`.

## Tests & coverage
```bash
pytest -v
pytest --cov=. --cov-report=term-missing
```
```
config.py                   15      0   100%
permissions.py              17      0   100%
routers/projects.py         46      0   100%
routers/tasks.py            38      0   100%
...
TOTAL                      492      0   100%
54 passed
```

## Docker & Render
```bash
docker build -t task-manager .
docker run --rm --env-file .env -p 8000:8000 task-manager
```
Render: **New + → Blueprint** with `render.yaml` (it asks for `ADMIN_EMAIL` / `ADMIN_PASSWORD`; `SECRET_KEY` is generated).
