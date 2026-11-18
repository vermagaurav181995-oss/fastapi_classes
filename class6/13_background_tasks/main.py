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

EMAIL_DELAY_SECONDS = 3
SENT_EMAILS: list[str] = []


def now() -> str:
    return datetime.now().strftime("%H:%M:%S")


def send_welcome_email(email: str) -> None:
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

    background_tasks.add_task(send_welcome_email, user.email)
    print(f"{now()} [route] response sent, the email is still pending")
    return user


@app.get("/emails/sent")
def sent_emails():
    return SENT_EMAILS
