from typing import Annotated

from fastapi import FastAPI, HTTPException, Path

app = FastAPI(title="Task 3 - solution")

BOOKS = {1: "Dune", 2: "1984"}


@app.get("/books/{book_id}")
def get_book(book_id: Annotated[int, Path(ge=1)]):
    if book_id not in BOOKS:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"id": book_id, "title": BOOKS[book_id]}
