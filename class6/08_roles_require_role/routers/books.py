"""
Books router with ROLES:
  GET    /books        -> public
  POST   /books        -> any logged-in user   (CurrentUser)
  DELETE /books/{id}   -> admins only          (AdminUser = require_role("admin"))
"""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from database import DbSession
from models import Book
from schemas import BookCreate, BookOut
from security import AdminUser, CurrentUser

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=list[BookOut])
def list_books(db: DbSession):
    return db.scalars(select(Book).order_by(Book.id)).all()


@router.post("", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(data: BookCreate, db: DbSession, user: CurrentUser):
    book = Book(title=data.title)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: DbSession, admin: AdminUser) -> None:
    # Reaching this line means: valid token (else 401) AND role == "admin" (else 403)
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.delete(book)
    db.commit()
