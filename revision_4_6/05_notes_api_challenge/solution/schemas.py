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


class NoteCreate(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=100)]
    content: Annotated[str, Field(max_length=5000)] = ""


class NoteUpdate(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    content: Annotated[str, Field(max_length=5000)] | None = None


class NoteOut(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
