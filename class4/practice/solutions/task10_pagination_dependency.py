from typing import Annotated

from fastapi import Depends, FastAPI, Query

app = FastAPI(title="Task 10 - solution")

BOOKS = [f"Book {n}" for n in range(1, 21)]
AUTHORS = [f"Author {n}" for n in range(1, 21)]


def pagination(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=10)] = 5,
) -> dict[str, int]:
    return {"skip": skip, "limit": limit}


PageDep = Annotated[dict[str, int], Depends(pagination)]


@app.get("/books")
def list_books(page: PageDep):
    return BOOKS[page["skip"] : page["skip"] + page["limit"]]


@app.get("/authors")
def list_authors(page: PageDep):
    return AUTHORS[page["skip"] : page["skip"] + page["limit"]]
