from typing import Annotated

from fastapi import Depends, FastAPI, Query

app = FastAPI(title="Task 11 - Pagination class")

BOOKS = [f"Book {n}" for n in range(1, 21)]
AUTHORS = [f"Author {n}" for n in range(1, 21)]


class Pagination:
    def __init__(self):
        pass


@app.get("/books")
def list_books():
    return BOOKS


@app.get("/authors")
def list_authors():
    return AUTHORS
