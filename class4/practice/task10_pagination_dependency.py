from typing import Annotated

from fastapi import Depends, FastAPI, Query

app = FastAPI(title="Task 10 - pagination dependency")

BOOKS = [f"Book {n}" for n in range(1, 21)]
AUTHORS = [f"Author {n}" for n in range(1, 21)]


def pagination():
    return {"skip": 0, "limit": 5}


@app.get("/books")
def list_books():
    return BOOKS


@app.get("/authors")
def list_authors():
    return AUTHORS
