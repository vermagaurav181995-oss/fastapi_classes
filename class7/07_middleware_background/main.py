import time
from typing import Annotated

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="07 - Middleware & Background Tasks")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time-ms"] = f"{(time.perf_counter() - start) * 1000:.2f}"
    return response


REGISTERED: set[str] = set()
sent_emails: list[str] = []


def send_welcome_email(email: str) -> None:
    sent_emails.append(email)
    print(f"[email] welcome email sent to {email}")


class Registration(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: Registration, background_tasks: BackgroundTasks):
    if data.email in REGISTERED:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    REGISTERED.add(data.email)
    background_tasks.add_task(send_welcome_email, data.email)
    return {"email": data.email}
