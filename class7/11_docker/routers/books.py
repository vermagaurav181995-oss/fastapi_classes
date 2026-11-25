from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, status

from schemas import BookIn, BookOut
from security import AdminUser, CurrentUser
from storage import BOOKS, next_id

router = APIRouter(prefix="/books", tags=["books"])

BookId = Annotated[int, Path(ge=1)]


def get_book_or_404(book_id: int) -> dict:
    if book_id not in BOOKS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return BOOKS[book_id]


@router.get("", response_model=list[BookOut])
def list_books(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return list(BOOKS.values())[skip : skip + limit]


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: BookId):
    return get_book_or_404(book_id)


@router.post("", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book: BookIn, user: CurrentUser):
    book_id = next_id(BOOKS)
    BOOKS[book_id] = {"id": book_id, **book.model_dump()}
    return BOOKS[book_id]


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: BookId, admin: AdminUser) -> None:
    get_book_or_404(book_id)
    del BOOKS[book_id]
