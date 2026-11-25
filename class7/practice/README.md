# Class 7: Practice Tasks

The practice folder contains the **bookstore with auth** app (same as 05–08) plus `chat.py` (same as 13).
`conftest.py` gives you `client` and an autouse `reset_data` fixture (task 3 asks you to write your own).
Each starter has `TODO` comments and its tests call `pytest.skip("TODO")`, so the suite passes until you fill them in.

## Run
```bash
cd practice
pytest -v                          # all starters (skipped until you do them)
pytest -v test_task02_books.py     # one task
pytest -v task03_conftest          # task 3 lives in its own folder (its own conftest.py)
```
Solutions:
```bash
cd practice/solutions
pytest -v
pytest --cov=.. --cov-report=term-missing
```

| # | Task | Starter | Example |
|---|---|---|---|
| 1 | `test_math.py`, one test failing on purpose | `test_task01_math.py` | 01 |
| 2 | `GET /books/{id}`: 200, 404, 422 | `test_task02_books.py` | 02 |
| 3 | `conftest.py` with an autouse reset fixture + a client fixture | `task03_conftest/` | 03 |
| 4 | parametrize with 5+ invalid payloads | `test_task04_parametrize.py` | 04 |
| 5 | `auth_headers` helper; register, 409, 401 | `test_task05_auth.py` | 05 |
| 6 | `/auth/me` with no token, fake token, real token | `test_task06_me.py` | 05 |
| 7 | admin-only route: 401 / 403 / 204 | `test_task07_admin.py` | 05 |
| 8 | `dependency_overrides` in a fixture that clears it | `test_task08_overrides.py` | 06 |
| 9 | timing header, CORS allowed / blocked | `test_task09_middleware.py` | 07 |
| 10 | reach 80%+ coverage | `task10_coverage.md` + `test_task10_coverage.py` | 08 |
| 11 | `--workers 2` and the in-memory problem | `task11_workers.md` | 10 |
| 12 | Dockerfile + .dockerignore | `task12_docker/` | 11 |
| 13 | deploy to Render (checklist) | `task13_render_checklist.md` | 12 |
| 14 | WebSocket chat test | `test_task14_websocket.py` | 13 |

Expected output once you've done everything: like `solutions/`, which gives `37 passed, 1 xfailed` (the xfail is task 1's test that fails on purpose).
