"""
13 - Background tasks
=====================
Some work shouldn't make the user wait (sending an email, resizing an image).
`BackgroundTasks` runs a function AFTER the response has been sent:
    background_tasks.add_task(send_welcome_email, user.email)
The client gets its 201 immediately; the "email" finishes ~3 seconds later.
(For heavy or must-not-be-lost jobs, use a real queue such as Celery or RQ.)

Setup:  cp .env.example .env
Run:    fastapi dev main.py   and watch the terminal
"""

import time
from datetime import datetime

from fastapi import BackgroundTasks, FastAPI, HTTPException, status
from sqlalchemy import select

from database import Base, DbSession, engine
from models import User
from schemas import UserCreate, UserOut
from security import hash_password

Base.metadata.create_all(bind=engine)
app = FastAPI(title="13 - Background Tasks")

EMAIL_DELAY_SECONDS = 3  # pretend the email server is slow
SENT_EMAILS: list[str] = []  # so we can check what was "sent"


def now() -> str:
    return datetime.now().strftime("%H:%M:%S")


def send_welcome_email(email: str) -> None:
    """Fake email sender. A plain `def` -> FastAPI runs it in a thread."""
    print(f"{now()} [email] sending welcome email to {email} ...")
    time.sleep(EMAIL_DELAY_SECONDS)
    SENT_EMAILS.append(email)
    print(f"{now()} [email] DONE: welcome email sent to {email}")


@app.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: DbSession, background_tasks: BackgroundTasks):
    if db.scalar(select(User).where(User.email == data.email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = User(email=data.email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    # Queue the job. It runs only if the route SUCCEEDS (no email after a 409).
    background_tasks.add_task(send_welcome_email, user.email)
    print(f"{now()} [route] response sent, the email is still pending")
    return user


@app.get("/emails/sent")
def sent_emails():
    return SENT_EMAILS


# ---------------------------------------------------------------------------
# TRY IT
# ---------------------------------------------------------------------------
# POST /auth/register {"email": "ada@example.com", "password": "supersecret"}
#   -> 201 IMMEDIATELY (it does not wait 3 seconds)
#   terminal:  12:00:00 [route] response sent, the email is still pending
#              12:00:00 [email] sending welcome email to ada@example.com ...
#              12:00:03 [email] DONE: welcome email sent to ada@example.com
# GET /emails/sent  right away    -> 200 []
# GET /emails/sent  3 s later     -> 200 ["ada@example.com"]
#
# These should FAIL (and no email is queued):
# same register request again        -> 409 "Email already registered"
# {"email": "x@example.com", "password": "short"} -> 422
