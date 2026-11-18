from typing import Annotated

from fastapi import FastAPI, HTTPException, status
from pwdlib import PasswordHash
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="Bug 05 - storing passwords (buggy)")

password_hash = PasswordHash.recommended()
USERS: dict[str, dict] = {}


class Credentials(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]


@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(data: Credentials):
    if data.email in USERS:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    USERS[data.email] = {"email": data.email, "password": data.password}
    return {"email": data.email}


@app.post("/auth/check-password")
def check_password(data: Credentials):
    user = USERS.get(data.email)
    if user is None or not user["password"] == data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    return {"message": "Password is correct"}


@app.get("/debug/storage")
def show_storage():
    return USERS
