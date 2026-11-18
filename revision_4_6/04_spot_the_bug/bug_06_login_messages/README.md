# Bug 06: The login page helps attackers

## Symptom
An attacker found out which emails have an account on our site, without knowing any passwords.

## Reproduce it
1. `POST /auth/login` form `username=nobody@example.com&password=whatever`
2. `POST /auth/login` form `username=ada@example.com&password=whatever`
3. Compare the two responses (status code **and** message). What does an attacker learn?

## Expected behavior
Both requests get exactly the same response.

## Run it
```bash
cd bug_06_login_messages/buggy
fastapi dev main.py
```
When you think you've found the bug, compare with `fixed/` (same command, from `bug_06_login_messages/fixed`) and check `../ANSWERS.md`.
