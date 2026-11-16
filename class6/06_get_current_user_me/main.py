"""
06 - get_current_user and GET /auth/me
======================================
security.py now has the key dependency chain:
    oauth2_scheme     -> reads "Authorization: Bearer <token>" (401 if missing)
    get_current_user  -> decodes the token, loads the user, checks is_active
    CurrentUser       -> Annotated[User, Depends(get_current_user)]
Any route that takes `user: CurrentUser` is now protected.

Setup:  cp .env.example .env
Run:    fastapi dev main.py         Docs: http://127.0.0.1:8000/docs
"""

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from database import Base, DbSession, engine
from models import User
from schemas import Token, UserCreate, UserOut
from security import CurrentUser, create_access_token, hash_password, verify_password

Base.metadata.create_all(bind=engine)
app = FastAPI(title="06 - Current User & /me")


@app.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: DbSession):
    if db.scalar(select(User).where(User.email == data.email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = User(email=data.email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/auth/login", response_model=Token)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    user = db.scalar(select(User).where(User.email == form.username))
    if user is None or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(user.id))


@app.get("/auth/me", response_model=UserOut)
def read_me(user: CurrentUser):
    # If we get here, the token was valid and `user` is a real, active User row
    return user


# ---------------------------------------------------------------------------
# TRY IT
# ---------------------------------------------------------------------------
# 1. POST /auth/register {"email": "ada@example.com", "password": "supersecret"} -> 201
# 2. POST /auth/login FORM username=ada@example.com&password=supersecret -> 200 {access_token}
# 3. GET  /auth/me   header  Authorization: Bearer <access_token>
#      -> 200 {"id": 1, "email": "ada@example.com", "role": "user", "is_active": true}
#
# These should FAIL:
# GET /auth/me  (no Authorization header)           -> 401 "Not authenticated"
# GET /auth/me  Authorization: Bearer fake.token.x  -> 401 "Could not validate credentials"
# GET /auth/me  with an EXPIRED token (set ACCESS_TOKEN_EXPIRE_MINUTES=1 in .env,
#               log in, wait 1 minute)              -> 401 "Could not validate credentials"
