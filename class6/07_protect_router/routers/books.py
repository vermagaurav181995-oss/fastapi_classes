from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from security import CurrentUser, get_current_user

router = APIRouter(
    prefix="/books",
    tags=["books (login required)"],
    dependencies=[Depends(get_current_user)],
)

BOOKS = [
    {"id": 1, "title": "Dune", "added_by": "system"},
    {"id": 2, "title": "1984", "added_by": "system"},
]


class BookIn(BaseModel):
    title: str


@router.get("")
def list_books():
    return BOOKS


@router.get("/{book_id}")
def get_book(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router.post("", status_code=status.HTTP_201_CREATED)
def add_book(data: BookIn, user: CurrentUser):
    book = {"id": len(BOOKS) + 1, "title": data.title, "added_by": user.email}
    BOOKS.append(book)
    return book
