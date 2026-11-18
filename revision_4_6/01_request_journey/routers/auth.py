from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from security import CurrentUser, create_access_token, verify_password
from storage import find_user_by_email

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = find_user_by_email(form.username)
    if user is None or not verify_password(form.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": create_access_token(user["id"]), "token_type": "bearer"}


@router.get("/me")
def read_me(user: CurrentUser):
    return {"id": user["id"], "email": user["email"], "role": user["role"]}
