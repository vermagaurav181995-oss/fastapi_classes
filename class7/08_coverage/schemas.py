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


class BookIn(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    price: Annotated[float, Field(gt=0)]


class BookOut(BaseModel):
    id: int
    title: str
    price: float
