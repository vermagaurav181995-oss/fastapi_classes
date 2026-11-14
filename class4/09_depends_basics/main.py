from typing import Annotated

from fastapi import Depends, FastAPI, Query

app = FastAPI(title="09 - Depends Basics")

BOOKS = [f"Book {n}" for n in range(1, 31)]
AUTHORS = [f"Author {n}" for n in range(1, 13)]


def pagination(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=20)] = 5,
) -> dict[str, int]:
    return {"skip": skip, "limit": limit}


PageDep = Annotated[dict[str, int], Depends(pagination)]


@app.get("/books")
def list_books(page: PageDep):
    start = page["skip"]
    return {"pagination": page, "total": len(BOOKS), "items": BOOKS[start : start + page["limit"]]}


@app.get("/authors")
def list_authors(page: Annotated[dict[str, int], Depends(pagination)]):
    start = page["skip"]
    return {"pagination": page, "total": len(AUTHORS), "items": AUTHORS[start : start + page["limit"]]}
