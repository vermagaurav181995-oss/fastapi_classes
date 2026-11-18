# Bug 07: Normal users are told to log in again

## Symptom
A normal user who tries to delete a book gets a "please log in" response, so the frontend sends them back to the login page in a loop, even though they *are* logged in.

## Reproduce it
1. `GET /books` with header `X-Token: user-token` → 200 (the token works).
2. `DELETE /books/1` with header `X-Token: user-token` → look at the status code.
3. Compare it with `DELETE /books/1` and **no** token. Can the frontend tell the two cases apart?

## Expected behavior
No token → 401; a valid user token on an admin-only route → a different status code meaning *not allowed*.

## Run it
```bash
cd bug_07_admin_401/buggy
fastapi dev main.py
```
When you think you've found the bug, compare with `fixed/` (same command, from `bug_07_admin_401/fixed`) and check `../ANSWERS.md`.
