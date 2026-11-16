"""/authors: public reads, logged-in users create, admins delete."""

from fastapi import APIRouter, status
from sqlalchemy import select

from database import DbSession
from exceptions import ConflictError, NotFoundError
from models import Author
from schemas import AuthorCreate, AuthorOut, BookOut
from security import AdminUser, CurrentUser

router = APIRouter(prefix="/authors", tags=["authors"])


def get_author_or_404(author_id: int, db) -> Author:
    author = db.get(Author, author_id)
    if author is None:
        raise NotFoundError("Author", author_id)
    return author


@router.get("", response_model=list[AuthorOut])
def list_authors(db: DbSession):
    return db.scalars(select(Author).order_by(Author.name)).all()


@router.get("/{author_id}", response_model=AuthorOut)
def get_author(author_id: int, db: DbSession):
    return get_author_or_404(author_id, db)


@router.get("/{author_id}/books", response_model=list[BookOut])
def get_author_books(author_id: int, db: DbSession):
    return get_author_or_404(author_id, db).books


@router.post("", response_model=AuthorOut, status_code=status.HTTP_201_CREATED)
def create_author(data: AuthorCreate, db: DbSession, user: CurrentUser):
    if db.scalar(select(Author).where(Author.name == data.name)):
        raise ConflictError(f"Author '{data.name}' already exists")
    author = Author(name=data.name)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: DbSession, admin: AdminUser) -> None:
    db.delete(get_author_or_404(author_id, db))  # cascade deletes their books too
    db.commit()
