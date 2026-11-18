from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from schemas import UserCreate
from security import CurrentUser

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: UserCreate):
    raise NotImplementedError


@router.post("/login")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    raise NotImplementedError


@router.get("/me")
def read_me(user: CurrentUser):
    raise NotImplementedError
