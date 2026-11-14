from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task 7 - PATCH")


class Book(BaseModel):
    title: str
    author: str
    price: float


BOOKS: dict[int, Book] = {1: Book(title="Dune", author="Frank Herbert", price=9.99)}


@app.patch("/books/{book_id}")
def update_book(book_id: int):
    return {"todo": "implement me"}
