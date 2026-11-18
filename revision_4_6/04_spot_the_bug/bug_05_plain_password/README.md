# Bug 05: The storage leak was worse than it should have been

## Symptom
Someone got a copy of our user storage. Security says that alone should **not** have let them log in as our users. But it did.

## Reproduce it
1. `POST /auth/register` `{"email": "ada@example.com", "password": "supersecret"}`
2. `GET /debug/storage` (pretend this is the leaked copy). Look at what's stored.
3. Could you log in as Ada with only what you see there?

## Expected behavior
The leaked storage contains nothing you could log in with directly.

## Run it
```bash
cd bug_05_plain_password/buggy
fastapi dev main.py
```
When you think you've found the bug, compare with `fixed/` (same command, from `bug_05_plain_password/fixed`) and check `../ANSWERS.md`.
