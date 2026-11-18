from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from common import DbSession, User, create_access_token, seed_demo_users, settings, verify_password

seed_demo_users()
app = FastAPI(title="Task 5 - solution")


@app.post("/auth/login")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    user = db.scalar(select(User).where(User.email == form.username))
    if user is None or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user.id)
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    print("token payload:", payload)
    return {"access_token": token, "token_type": "bearer"}
