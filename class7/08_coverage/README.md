# 08: Coverage

## What it shows
The app is the **in-memory bookstore with auth** from Class 6 (`config.py`, `storage.py`, `security.py`, `emails.py`, `routers/`, `main.py`). A lifespan seeds the admin `admin@example.com` / `admin12345` from `ADMIN_EMAIL` / `ADMIN_PASSWORD`.
`conftest.py` sets `SECRET_KEY` (≥ 32 characters), `ADMIN_EMAIL` and `ADMIN_PASSWORD` with `os.environ` **before** importing the app, because `config.py` reads them at import time.

Tests live in a `tests/` folder (`conftest.py`, `test_books.py`, `test_auth.py`, `test_middleware.py`). `pytest.ini` has `pythonpath = .` (so `import main` works from `tests/`) and `testpaths = tests`.

## Setup
No `.env` needed for the tests.

## Run
```bash
cd 08_coverage
pytest -v
pytest --cov=. --cov-report=term-missing
pytest --cov=. --cov-report=html          # then open htmlcov/index.html: covered lines green, missed lines red
pytest --cov=. --cov-fail-under=90        # fail the run if coverage drops below 90%
```

## Expected output
```
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
config.py                     10      0   100%
emails.py                     10      0   100%
main.py                       28      0   100%
routers/auth.py               24      0   100%
routers/books.py              26      0   100%
security.py                   39      0   100%
storage.py                    17      0   100%
...
TOTAL                        285      0   100%
30 passed
```
### Reading the Missing column
- **Stmts**: lines of code that can run · **Miss**: how many never ran · **Cover**: the percentage
- **Missing**: the **line numbers** that never ran, e.g. `security.py  39  3  92%  48-49, 52`
- Try it: comment out `test_me_after_user_was_deleted_returns_401` in `tests/test_auth.py`, run again, and `security.py` shows the `raise invalid_credentials` line after `if user is None:` as Missing. Then you know which test to write.
- 100% coverage doesn't mean bug-free: it only means every line ran. You still need good **asserts**.
