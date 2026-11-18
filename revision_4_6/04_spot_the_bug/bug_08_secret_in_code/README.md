# Bug 08: Someone became admin without logging in

## Symptom
Our code is on a public GitHub repo. Someone who never called `/auth/login` sent requests that `/auth/me` accepted as user id **1** (the admin).

## Reproduce it
1. Log in normally: `POST /auth/login` form `username=ada@example.com&password=supersecret` → `GET /auth/me` says `user_id: 2`.
2. Now act like the attacker: you can read every file in `buggy/`, but you can't log in as the admin.
3. Using only what's in those files (and `pip install pyjwt`), can you build a token that `GET /auth/me` accepts as user 1?

## Expected behavior
Files from the repo are not enough to create a valid token.

## Run it
```bash
cd bug_08_secret_in_code/buggy
fastapi dev main.py
```
When you think you've found the bug, compare with `fixed/` (same command, from `bug_08_secret_in_code/fixed`) and check `../ANSWERS.md`.

`fixed/` needs a `.env`: `cp .env.example .env` (inside `fixed/`), then set `SECRET_KEY` to the output of `python -c "import secrets; print(secrets.token_hex(32))"`.
