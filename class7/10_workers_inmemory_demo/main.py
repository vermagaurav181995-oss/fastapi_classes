import os
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(title="10 - Workers & in-memory data")

USERS: dict[str, dict] = {}


class Registration(BaseModel):
    username: Annotated[str, Field(min_length=2, max_length=30)]


@app.get("/pid")
def get_pid():
    return {"pid": os.getpid(), "users_on_this_worker": len(USERS)}


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: Registration):
    USERS[data.username] = {"username": data.username, "registered_on_pid": os.getpid()}
    return {**USERS[data.username], "answered_by_pid": os.getpid()}


@app.get("/whoami")
def whoami(username: Annotated[str, Query(min_length=2)]):
    if username not in USERS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"'{username}' is unknown to worker {os.getpid()}",
        )
    return {**USERS[username], "answered_by_pid": os.getpid()}
