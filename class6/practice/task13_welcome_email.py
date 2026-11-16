"""
Task 13 - Welcome email in the background
After a successful register, queue send_welcome_email(email) with BackgroundTasks.
The response must come back IMMEDIATELY; the email prints ~3 seconds later.
Run:  fastapi dev task13_welcome_email.py
"""

import time
from typing import Annotated

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select

from common import Base, DbSession, User, engine, hash_password

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Task 13 - background email")

EMAIL_DELAY_SECONDS = 3
SENT_EMAILS: list[str] = []


def send_welcome_email(email: str) -> None:
    time.sleep(EMAIL_DELAY_SECONDS)
    SENT_EMAILS.append(email)
    print(f"[email] welcome email sent to {email}")


class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]


@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: DbSession):  # TODO: add background_tasks: BackgroundTasks
    if db.scalar(select(User).where(User.email == data.email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = User(email=data.email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    # TODO: background_tasks.add_task(send_welcome_email, user.email)
    return {"id": user.id, "email": user.email}
