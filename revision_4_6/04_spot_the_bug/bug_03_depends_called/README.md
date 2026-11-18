# Bug 03: Pagination is stuck on page 1

## Symptom
The book list always shows Book 1–5, no matter which `skip` or `limit` you send.

## Reproduce it
1. `GET /books?skip=10&limit=3` → still `Book 1` … `Book 5` with `{"skip": 0, "limit": 5}`.
2. `GET /books?limit=500` should be rejected (limit max is 20), but it returns 200.
3. Open `/docs` → **GET /books**: where did `skip` and `limit` go? What does Swagger show instead?

## Expected behavior
`GET /books?skip=10&limit=3` → `Book 11`–`Book 13`; `?limit=500` → 422.

## Run it
```bash
cd bug_03_depends_called/buggy
fastapi dev main.py
```
When you think you've found the bug, compare with `fixed/` (same command, from `bug_03_depends_called/fixed`) and check `../ANSWERS.md`.
