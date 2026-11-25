# Capstone Project: Build, Test & Deploy Your Own API

Build a complete REST API with FastAPI that uses everything from the course: routers, validation, dependency injection, authentication, roles, tests, Docker and a live deployment.
Data lives in Python dicts (no database). That's fine for this project: say so in your README.

Start from [`template/`](template/). Auth is already complete and tested. [`example_task_manager/`](example_task_manager/) is a full reference solution for idea 1.

---

## Must-have (all required)
1. **Auth:** register (201, 409 duplicate email, 422 invalid), login with OAuth2 form → JWT (`sub` = user id as a string, plus `exp`), `GET /auth/me`. Passwords hashed with **pwdlib**, never returned.
2. **Your main resource with full CRUD:** create (201), list, read, update with **PATCH** + `model_dump(exclude_unset=True)`, delete (204).
3. **Ownership:** users only see and change **their own** data (403 otherwise, 404 for missing items).
4. **Roles:** an `admin` role via `require_role("admin")`, with at least one admin-only route. The first admin is created in the **lifespan** from `.env`.
5. **Validation:** `Path` / `Query` / `Field` constraints, so bad input gets a 422.
6. **Pagination** with a dependency (`skip` / `limit`) on every list route.
7. **A custom exception + handler** (e.g. `NotFoundError` → `{"error": ..., "message": ...}`).
8. **Settings** from `.env` with pydantic-settings; `SECRET_KEY` required; `.env.example` committed, `.env` git-ignored.
9. **CORS** from settings, plus a **timing middleware** (`X-Process-Time-ms`).
10. **Tests:** at least **20 pytest tests**, with a fixture that resets the data, covering success **and** failure cases (401 / 403 / 404 / 409 / 422). **Coverage ≥ 80%.**
11. **Docker:** a working `Dockerfile` and `.dockerignore`.
12. **Deployed on Render** (or a similar platform), with `GET /health` and `/docs` hidden in production.
13. **README** with setup, run, test and deploy instructions, plus an endpoints table (public / user / admin).

## Nice-to-have (extra credit)
- Filters and search on list routes (`?status=`, `?q=`, date ranges)
- A second, related resource (projects → tasks, posts → comments)
- `BackgroundTasks` (e.g. a "welcome" or "reminder" email that is printed)
- `dependency_overrides` in your tests
- A WebSocket feature (live notifications, chat)
- A tiny frontend calling your API (CORS!)
- `docker-compose.yml`, a `render.yaml` blueprint, `--cov-fail-under=80` in CI (GitHub Actions)

---

## Project ideas (pick one, or propose your own)

| # | Idea | Main resources | Ideas for rules |
|---|---|---|---|
| 1 | **Task manager** | projects, tasks | tasks have status + due date; filter by status / due date; only the owner edits; admin sees all |
| 2 | **Blog** | posts, comments | anyone reads published posts; authors edit their own posts; comment owners or admins delete comments; drafts visible only to the author |
| 3 | **Expense tracker** | expenses, categories | amount > 0; filter by month and category; `GET /expenses/summary` totals per category; strictly private per user |
| 4 | **Library** | books, loans | admins add books; users borrow (409 if already loaned) and return; max 3 loans per user; overdue list for admins |
| 5 | **Event booking** | events, bookings | admins create events with capacity; users book seats (409 when full or already booked) and cancel; list upcoming events |
| 6 | **Recipe book** | recipes, ingredients/ratings | public recipes vs private ones; search by ingredient (`?q=`); users rate others' recipes 1–5 (not their own) |

---

## Deliverables
1. A **GitHub repository** (public, or shared with the teacher) with a clean commit history.
2. The **live URL** on Render, plus a working `/health`.
3. A **README.md** (start from the template's): description, endpoints table, setup / run / test / Docker / deploy commands, admin credentials for testing.
4. A **coverage report**: paste the `pytest --cov=. --cov-report=term-missing` output into the README.
5. A **5-minute demo**: register → login → CRUD → a 403 → an admin action → tests running.

---

## Grading rubric (100 points)

| Area | Points | What we look for |
|---|---|---|
| **Features** | 30 | Every must-have works; correct status codes; ownership and roles enforced; validation |
| **Code quality** | 20 | Clear structure (routers, schemas, security, dependencies); good names; no duplication; type hints; `Annotated` |
| **Tests** | 20 | 20+ meaningful tests; success and failure cases; reset fixture; auth helpers; coverage ≥ 80% |
| **Security** | 15 | Hashed passwords never returned; secrets only in `.env`; same 401 message for wrong email or password; 401 vs 403 used correctly; CORS restricted |
| **Deployment + Docker + README** | 10 | Image builds and runs; app live on Render; README lets someone else run it in 5 minutes |
| **Demo** | 5 | Clear, on time, shows auth and an error case |

**Automatic deductions:** a `SECRET_KEY` or `.env` committed to git (−10), tests that don't run (−10), a plain-text password stored anywhere (−10).
