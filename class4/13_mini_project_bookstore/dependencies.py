from typing import Annotated

from fastapi import Depends, Header, HTTPException, Path, Query, status

from db import BOOKS
from exceptions import BookNotFound

API_KEY = "bookstore-admin-key"


class Pagination:
    def __init__(
        self,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=50)] = 10,
    ):
        self.skip = skip
        self.limit = limit

    def apply(self, items: list) -> list:
        return items[self.skip : self.skip + self.limit]


PaginationDep = Annotated[Pagination, Depends()]


def get_book_or_404(book_id: Annotated[int, Path(ge=1)]) -> dict:
    if book_id not in BOOKS:
        raise BookNotFound(book_id)
    return BOOKS[book_id]


BookDep = Annotated[dict, Depends(get_book_or_404)]


def verify_api_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing API key")
