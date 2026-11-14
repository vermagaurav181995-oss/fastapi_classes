from fastapi import APIRouter, status

from db import AUTHORS, BOOKS, next_id
from dependencies import PaginationDep
from exceptions import AuthorNotFound
from models import AuthorIn, AuthorOut, BookOut

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("", response_model=list[AuthorOut])
def list_authors(page: PaginationDep):
    return page.apply(list(AUTHORS.values()))


@router.get("/{author_id}", response_model=AuthorOut)
def get_author(author_id: int):
    if author_id not in AUTHORS:
        raise AuthorNotFound(author_id)
    return AUTHORS[author_id]


@router.get("/{author_id}/books", response_model=list[BookOut])
def get_author_books(author_id: int):
    if author_id not in AUTHORS:
        raise AuthorNotFound(author_id)
    return [b for b in BOOKS.values() if b["author_id"] == author_id]


@router.post("", response_model=AuthorOut, status_code=status.HTTP_201_CREATED)
def create_author(data: AuthorIn):
    author_id = next_id(AUTHORS)
    AUTHORS[author_id] = {"id": author_id, **data.model_dump()}
    return AUTHORS[author_id]
