from typing import Annotated

from pydantic import BaseModel, Field


class AuthorIn(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50)]


class AuthorOut(BaseModel):
    id: int
    name: str


class BookCreate(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=100)]
    author_id: int
    price: Annotated[float, Field(gt=0)]
    stock: Annotated[int, Field(ge=0)] = 0
    cost_price: Annotated[float, Field(gt=0)]


class BookUpdate(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    author_id: int | None = None
    price: Annotated[float, Field(gt=0)] | None = None
    stock: Annotated[int, Field(ge=0)] | None = None


class BookOut(BaseModel):
    id: int
    title: str
    author_id: int
    price: float
    stock: int
    cover: str | None = None
