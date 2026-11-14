from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task 7 - solution")


class Book(BaseModel):
    title: str
    author: str
    price: float


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    price: float | None = None


BOOKS: dict[int, Book] = {1: Book(title="Dune", author="Frank Herbert", price=9.99)}


@app.patch("/books/{book_id}")
def update_book(book_id: int, changes: BookUpdate) -> Book:
    if book_id not in BOOKS:
        raise HTTPException(status_code=404, detail="Book not found")
    updated = BOOKS[book_id].model_copy(update=changes.model_dump(exclude_unset=True))
    BOOKS[book_id] = updated
    return updated
