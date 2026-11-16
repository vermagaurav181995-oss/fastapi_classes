"""Pydantic schemas = what the API accepts and returns."""

from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Role(StrEnum):
    user = "user"
    admin = "admin"


class UserCreate(BaseModel):  # what the client sends to /auth/register
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]


class UserOut(BaseModel):  # what we send back: NO password field at all
    model_config = ConfigDict(from_attributes=True)  # read from a SQLAlchemy object

    id: int
    email: str
    role: Role
    is_active: bool


class Token(BaseModel):  # the shape OAuth2 clients (and /docs) expect
    access_token: str
    token_type: str = "bearer"


class BookCreate(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]


class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
