from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Role(StrEnum):
    user = "user"
    admin = "admin"


class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]


class UserOut(ORMModel):
    id: int
    email: str
    role: Role
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PasswordChange(BaseModel):
    old_password: str
    new_password: Annotated[str, Field(min_length=8)]


class AuthorCreate(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=100)]


class AuthorOut(ORMModel):
    id: int
    name: str


class BookCreate(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    year: Annotated[int, Field(ge=0, le=2100)] | None = None
    author_id: int


class BookOut(ORMModel):
    id: int
    title: str
    year: int | None
    author_id: int


class ReviewCreate(BaseModel):
    rating: Annotated[int, Field(ge=1, le=5)]
    text: Annotated[str, Field(min_length=1, max_length=1000)]


class ReviewUpdate(BaseModel):
    rating: Annotated[int, Field(ge=1, le=5)] | None = None
    text: Annotated[str, Field(min_length=1, max_length=1000)] | None = None


class ReviewOut(ORMModel):
    id: int
    rating: int
    text: str
    book_id: int
    owner_id: int
