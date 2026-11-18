from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash

app = FastAPI(title="Bug 06 - login messages (buggy)")

password_hash = PasswordHash.recommended()
USERS = {"ada@example.com": {"email": "ada@example.com", "hashed_password": password_hash.hash("supersecret")}}


@app.post("/auth/login")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = USERS.get(form.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No account with this email")
    if not password_hash.verify(form.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")
    return {"access_token": f"fake-token-for-{user['email']}", "token_type": "bearer"}
