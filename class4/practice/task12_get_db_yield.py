from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI(title="Task 12 - yield dependency")


def get_db():
    db = {1: "Dune", 2: "1984"}
    return db


@app.get("/books/{book_id}")
def get_book(book_id: int):
    return {"todo": "implement me"}
