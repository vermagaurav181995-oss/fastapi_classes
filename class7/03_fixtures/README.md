# 03: Fixtures & conftest.py

## What it shows
- `conftest.py` is loaded automatically; its fixtures are available to every test in the folder.
- `reset_books` is **autouse**: it runs around every test. The code before `yield` is setup (clear + reseed), the code after `yield` is teardown.
- The `client` fixture uses `with TestClient(app) as c:`, which also runs the app's startup/shutdown (lifespan).
- `test_books.py` shows that data added or broken in one test is back to normal in the next one.

### The broken version: `without_fixture/`
The same app, **no reset fixture**. `test_2_add.py` adds a book and never cleans up, while `test_1_count.py` expects exactly 3 books. The result depends on the **order**.

## Setup
No `.env` needed.

## Run
```bash
cd 03_fixtures
pytest -v                                   # with the fixture: all pass, in any order

cd without_fixture
pytest -v -p no:randomly                    # default (file) order: count runs first, so it passes
pytest -v test_2_add.py test_1_count.py     # REVERSED order: test_there_are_three_books FAILS
pytest -v -k add                            # -k only SELECTS tests (no reordering): add alone passes
```
`-p no:randomly` disables the *pytest-randomly* plugin if it's installed (it shuffles test order on purpose to find exactly this kind of bug). Without the plugin the flag does nothing.

## Expected output
```
03_fixtures:                 6 passed
without_fixture (default):   2 passed
without_fixture (reversed):  FAILED test_1_count.py::test_there_are_three_books - AssertionError: assert 4 == 3
```
**Lesson:** every test must start from known data. Put the reset in an autouse fixture.
