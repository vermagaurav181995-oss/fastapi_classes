"""
Books router: the WHOLE router is protected.
dependencies=[Depends(get_current_user)] runs before EVERY route below, so a
request without a valid token never reaches them (401).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from security import CurrentUser, get_current_user

router = APIRouter(
    prefix="/books",
    tags=["books (login required)"],
    dependencies=[Depends(get_current_user)],  # <- protects every route here
)

# In-memory books, to keep the focus on protection (example 08 uses the DB)
BOOKS = [
    {"id": 1, "title": "Dune", "added_by": "system"},
    {"id": 2, "title": "1984", "added_by": "system"},
]


class BookIn(BaseModel):
    title: str


@router.get("")
def list_books():
    # No user parameter needed: the router dependency already checked the token
    return BOOKS


@router.get("/{book_id}")
def get_book(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router.post("", status_code=status.HTTP_201_CREATED)
def add_book(data: BookIn, user: CurrentUser):
    # Here we NEED the user's data, so we ask for CurrentUser explicitly.
    # (FastAPI caches the dependency: get_current_user still runs only once.)
    book = {"id": len(BOOKS) + 1, "title": data.title, "added_by": user.email}
    BOOKS.append(book)
    return book
