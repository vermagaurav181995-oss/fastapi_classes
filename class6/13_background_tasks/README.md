# 13: Background Tasks

## What is this?
`BackgroundTasks.add_task(send_welcome_email, email)` runs the function **after** the response is sent. The fake email sleeps 3 seconds, but `POST /auth/register` returns its 201 immediately. Tasks only run when the route succeeds (no email after a 409). For heavy or must-not-be-lost jobs, use a real queue such as Celery or RQ.

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste the output as SECRET_KEY in .env
```

## Run it
```bash
cd 13_background_tasks
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. Register a user and keep an eye on the **terminal**: the response comes first, and the email line appears 3 seconds later. Call **GET /emails/sent** before and after.

## TRY IT
1. `POST /auth/register` `{"email": "ada@example.com", "password": "supersecret"}` → 201 instantly
2. `GET /emails/sent` right away → `[]`; 3 s later → `["ada@example.com"]`
3. ❌ same email again → 409 (no email queued)
4. ❌ password `short` → 422

All requests are also in [`../test_requests.http`](../test_requests.http).
