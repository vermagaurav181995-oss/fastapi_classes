from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="07 - Status Codes & Response Models")


class UserIn(BaseModel):
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str


USERS: dict[int, dict] = {
    1: {"id": 1, "username": "alice", "email": "alice@example.com", "password": "a-secret"},
    2: {"id": 2, "username": "bob", "email": "bob@example.com", "password": "b-secret"},
}


@app.get("/users", response_model=list[UserOut])
def list_users():
    return list(USERS.values())


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id not in USERS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return USERS[user_id]


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserIn):
    new_id = max(USERS, default=0) + 1
    USERS[new_id] = {"id": new_id, **user.model_dump()}
    return USERS[new_id]


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int) -> None:
    if user_id not in USERS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    del USERS[user_id]
