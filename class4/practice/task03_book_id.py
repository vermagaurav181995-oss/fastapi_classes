from typing import Annotated

from fastapi import FastAPI, HTTPException, Path

app = FastAPI(title="Task 3 - book_id")

BOOKS = {1: "Dune", 2: "1984"}


@app.get("/books/{book_id}")
def get_book(book_id: int):
    return {"todo": "implement me"}
