from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from security import CurrentUser, create_access_token

app = FastAPI(title="Bug 08 - secret key (buggy)")

USERS = {"ada@example.com": {"id": 2, "email": "ada@example.com", "password": "supersecret", "role": "user"}}


@app.post("/auth/login")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = USERS.get(form.username)
    if user is None or user["password"] != form.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    return {"access_token": create_access_token(user["id"]), "token_type": "bearer"}


@app.get("/auth/me")
def read_me(user_id: CurrentUser):
    return {"user_id": user_id, "is_admin": user_id == 1}
