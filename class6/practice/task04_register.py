from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from common import Base, DbSession, User, engine, hash_password

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Task 4 - register")


class UserCreate(BaseModel):
    email: str
    password: str


@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: DbSession):
    return {"todo": "implement me"}
