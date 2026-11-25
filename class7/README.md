# Class 7: Testing, Deployment & Capstone

Runnable examples for testing FastAPI apps with pytest, preparing them for production, shipping them with Docker and Render, plus a WebSocket bonus and the capstone project.
No database: all data lives in Python dicts.

## Setup (once)
Requires **Python 3.11+** (and Docker for example 11).
```bash
cd class7
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
Apps that need secrets have a `.env.example`. Copy it to `.env` and set `SECRET_KEY` (32+ characters):
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"
```
Tests never need a `.env`: each `conftest.py` sets a test `SECRET_KEY` before importing the app.

## Examples
Run every command from **inside** the folder.

| # | Topic | Run |
|---|---|---|
| 01 | pytest basics, reading a failure | `cd 01_pytest_basics && pytest -v` |
| 02 | TestClient: status codes + json / params / headers / data / files / cookies | `cd 02_testclient_basics && pytest -v` |
| 03 | fixtures, conftest.py, autouse reset (+ the broken `without_fixture/`) | `cd 03_fixtures && pytest -v` · `cd 03_fixtures/without_fixture && pytest -v test_2_add.py test_1_count.py` |
| 04 | `@pytest.mark.parametrize` | `cd 04_parametrize && pytest -v` |
| 05 | testing auth: register, login, me, expired tokens, 401/403/204 | `cd 05_testing_auth && pytest -v` |
| 06 | `app.dependency_overrides` in fixtures | `cd 06_dependency_overrides && pytest -v` |
| 07 | testing middleware, CORS, background tasks | `cd 07_middleware_background && pytest -v` |
| 08 | coverage with pytest-cov | `cd 08_coverage && pytest --cov=. --cov-report=term-missing` |
| 09 | production settings, hiding /docs, `dev` vs `run` vs `--workers` | `cd 09_production_settings && fastapi dev main.py` · `pytest -v` |
| 10 | why in-memory data breaks with workers | `cd 10_workers_inmemory_demo && fastapi run main.py --workers 2` |
| 11 | Docker + docker compose | `cd 11_docker && docker build -t bookstore . && docker run --rm --env-file .env -p 8000:8000 bookstore` |
| 12 | deploy to Render (`render.yaml`, `/health`, checklist) | `cd 12_deploy_render && fastapi dev main.py` |
| 13 | WebSocket chat + testing it | `cd 13_websocket_chat && fastapi dev main.py` · `pytest -v` |
| 14 | Capstone: brief, template, reference solution | `14_capstone/CAPSTONE.md` · `cd 14_capstone/template && pytest -v` · `cd 14_capstone/example_task_manager && pytest -v` |
| P | Practice tasks (+ solutions) | `cd practice && pytest -v` · `cd practice/solutions && pytest -v` |

Every app folder can also be started with `fastapi dev main.py` (copy its `.env.example` first if it has one).

## Run every test folder
```bash
./run_all_tests.sh
```
It runs pytest in all 15 test folders one after another and prints a PASS/FAIL summary.
