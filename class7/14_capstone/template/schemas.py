from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]


class UserOut(BaseModel):
    id: int
    email: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ItemCreate(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]


class ItemUpdate(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)] | None = None


class ItemOut(BaseModel):
    id: int
    name: str
    owner_id: int
