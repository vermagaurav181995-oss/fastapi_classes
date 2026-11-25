# Solution 10: Reach 80%+ coverage

Run from `practice/solutions/`:
```bash
pytest --cov=.. --cov-report=term-missing
```
`--cov=..` measures the app in `practice/`. With all the solution tests every **app module** (`main.py`, `security.py`, `routers/…`, `chat.py`, …) is at **100%**.
The TOTAL line shows about 80%, because `--cov=..` also counts the unfinished starter test files in `practice/` (their bodies are skipped). Once you've completed the starters, the TOTAL goes up too.

What the Missing column pointed to, and the test that covers it:
- `main.py` `root()`: `GET /`
- `routers/books.py` `create_book` and the 404 in `delete_book`: POST as a logged-in user, DELETE `/books/999` as admin
- `routers/books.py` `skip`/`limit` slicing: `GET /books?skip=1&limit=1`
- `security.py` `if user is None`: a valid token for a user that no longer exists
- `emails.py` `EmailSender.send`: register a user, then check `SENT_EMAILS`

Fail the run when coverage drops: `pytest --cov=.. --cov-fail-under=80`.
