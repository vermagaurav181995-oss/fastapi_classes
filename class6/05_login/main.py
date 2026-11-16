"""
05 - Login: email + password -> access token
============================================
OAuth2PasswordRequestForm reads a FORM body (not JSON) with the fields
`username` and `password`. That's the OAuth2 standard, and it's what the
/docs "Authorize" button sends. We put the EMAIL in the `username` field.

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
from security import create_access_token, hash_password, verify_password

Base.metadata.create_all(bind=engine)
app = FastAPI(title="05 - Login")


@app.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: DbSession):  # same as example 03
    if db.scalar(select(User).where(User.email == data.email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = User(email=data.email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/auth/login", response_model=Token)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    # Step 1: find the user by email (sent in the "username" field)
    user = db.scalar(select(User).where(User.email == form.username))

    # Step 2: SAME error for "no such email" and "wrong password", so an
    # attacker can't find out which emails are registered.
    if user is None or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},  # the standard 401 header
        )

    # Step 3: give the client a signed token with "sub" = the user id
    return Token(access_token=create_access_token(user.id))


# ---------------------------------------------------------------------------
# TRY IT
# ---------------------------------------------------------------------------
# POST /auth/register {"email": "ada@example.com", "password": "supersecret"} -> 201
# POST /auth/login   FORM username=ada@example.com&password=supersecret
#   -> 200 {"access_token": "eyJhbGciOi...", "token_type": "bearer"}
# In /docs: click "Authorize", type the email as username + the password -> "Authorized"
#
# These should FAIL (note: the SAME message for both):
# login with password=wrongpass          -> 401 "Incorrect email or password"
# login with username=nobody@example.com -> 401 "Incorrect email or password"
#   (both responses carry the header  WWW-Authenticate: Bearer)
# login with a JSON body instead of a form -> 422 "Field required"
