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


class ReviewCreate(BaseModel):
    book_title: Annotated[str, Field(min_length=1, max_length=200)]
    text: Annotated[str, Field(min_length=1, max_length=1000)]
    rating: Annotated[int, Field(ge=1, le=5)]


class ReviewUpdate(BaseModel):  # PATCH: everything optional
    text: Annotated[str, Field(min_length=1, max_length=1000)] | None = None
    rating: Annotated[int, Field(ge=1, le=5)] | None = None


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_title: str
    text: str
    rating: int
    owner_id: int
