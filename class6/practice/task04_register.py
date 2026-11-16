"""
Task 4 - POST /auth/register
* email must be valid (EmailStr), password at least 8 chars
* 409 if the email is already registered
* the response must NOT contain the password or the hash
Run:  fastapi dev task04_register.py
"""

from fastapi import FastAPI, HTTPException, status  # noqa: F401
from pydantic import BaseModel
from sqlalchemy import select  # noqa: F401

from common import Base, DbSession, User, engine, hash_password  # noqa: F401

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Task 4 - register")


class UserCreate(BaseModel):
    email: str  # TODO: EmailStr
    password: str  # TODO: at least 8 characters


# TODO: class UserOut(BaseModel) with id, email, role  (from_attributes=True)


@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: DbSession):
    # TODO: 409 if a User with this email exists
    # TODO: create User(email=..., hashed_password=hash_password(...)), commit, refresh
    # TODO: return the user through response_model=UserOut
    return {"todo": "implement me"}
