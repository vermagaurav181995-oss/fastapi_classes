from typing import Annotated

from fastapi import Depends, FastAPI, Query

app = FastAPI(title="Task 11 - solution")

BOOKS = [f"Book {n}" for n in range(1, 21)]
AUTHORS = [f"Author {n}" for n in range(1, 21)]


class Pagination:
    def __init__(
        self,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=10)] = 5,
    ):
        self.skip = skip
        self.limit = limit

    def apply(self, items: list) -> list:
        return items[self.skip : self.skip + self.limit]


PaginationDep = Annotated[Pagination, Depends()]


@app.get("/books")
def list_books(page: PaginationDep):
    return page.apply(BOOKS)


@app.get("/authors")
def list_authors(page: PaginationDep):
    return page.apply(AUTHORS)
