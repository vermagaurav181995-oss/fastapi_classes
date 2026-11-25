# Task 10: Reach 80%+ coverage

1. From `practice/`, run:
   ```bash
   pytest --cov=. --cov-report=term-missing
   ```
2. Look at the **Missing** column: those line numbers never ran during the tests.
3. Open each file and find out which request would run those lines. *TODO: write your notes here:*
   - `routers/books.py` lines …: …
   - `security.py` lines …: …
4. Add tests to `test_task10_coverage.py` until the **TOTAL** is 80% or more.
5. Bonus: make pytest fail when coverage drops: `pytest --cov=. --cov-fail-under=80`.
