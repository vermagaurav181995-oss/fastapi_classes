"""/books: public reads (with pagination), logged-in users create, admins delete."""

from typing import Annotated

from fastapi import APIRouter, Query, status
from sqlalchemy import select

from database import DbSession
from exceptions import NotFoundError
from models import Author, Book
from schemas import BookCreate, BookOut
from security import AdminUser, CurrentUser

router = APIRouter(prefix="/books", tags=["books"])


def get_book_or_404(book_id: int, db) -> Book:
    book = db.get(Book, book_id)
    if book is None:
        raise NotFoundError("Book", book_id)
    return book


@router.get("", response_model=list[BookOut])
def list_books(
    db: DbSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    author_id: int | None = None,
):
    query = select(Book).order_by(Book.id).offset(skip).limit(limit)
    if author_id is not None:
        query = query.where(Book.author_id == author_id)
    return db.scalars(query).all()


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: DbSession):
    return get_book_or_404(book_id, db)


@router.post("", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(data: BookCreate, db: DbSession, user: CurrentUser):
    if db.get(Author, data.author_id) is None:
        raise NotFoundError("Author", data.author_id)
    book = Book(**data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: DbSession, admin: AdminUser) -> None:
    db.delete(get_book_or_404(book_id, db))
    db.commit()
