from typing import Annotated

from fastapi import Depends, FastAPI, Query

app = FastAPI(title="Bug 03 - pagination dependency (fixed)")

BOOKS = [f"Book {n}" for n in range(1, 31)]


def pagination(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=20)] = 5,
) -> dict[str, int]:
    return {"skip": skip, "limit": limit}


@app.get("/books")
def list_books(page: Annotated[dict[str, int], Depends(pagination)]):
    start = page["skip"]
    return {"page": page, "items": BOOKS[start : start + page["limit"]]}
