# Bug 04: Database connections are never released

## Symptom
Under load the (fake) database runs out of connections. Every request opens one and none come back.

## Reproduce it
1. Call `GET /books` three times.
2. Call `GET /health` → `{"open_connections": 3}`, and it keeps growing with every request.
3. Watch the terminal: you see `opened` lines but never a `closed` line.

## Expected behavior
After any number of `GET /books`, `GET /health` → `{"open_connections": 0}`; the terminal prints `opened` and then `closed`.

## Run it
```bash
cd bug_04_connection_cleanup/buggy
fastapi dev main.py
```
When you think you've found the bug, compare with `fixed/` (same command, from `bug_04_connection_cleanup/fixed`) and check `../ANSWERS.md`.
