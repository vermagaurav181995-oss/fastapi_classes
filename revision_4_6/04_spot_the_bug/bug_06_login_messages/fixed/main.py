from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash

app = FastAPI(title="Bug 06 - login messages (fixed)")

password_hash = PasswordHash.recommended()
USERS = {"ada@example.com": {"email": "ada@example.com", "hashed_password": password_hash.hash("supersecret")}}


@app.post("/auth/login")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = USERS.get(form.username)
    if user is None or not password_hash.verify(form.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": f"fake-token-for-{user['email']}", "token_type": "bearer"}
