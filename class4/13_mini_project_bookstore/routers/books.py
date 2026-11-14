from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, UploadFile, status

from db import AUTHORS, BOOKS, UPLOAD_DIR, next_id
from dependencies import BookDep, PaginationDep
from exceptions import AuthorNotFound
from models import BookCreate, BookOut, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])

IMAGE_TYPES = {"image/png": ".png", "image/jpeg": ".jpg"}


@router.get("", response_model=list[BookOut])
def list_books(page: PaginationDep, author_id: Annotated[int | None, Query(ge=1)] = None):
    books = list(BOOKS.values())
    if author_id is not None:
        books = [b for b in books if b["author_id"] == author_id]
    return page.apply(books)


@router.get("/{book_id}", response_model=BookOut)
def get_book(book: BookDep):
    return book


@router.post("", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(data: BookCreate):
    if data.author_id not in AUTHORS:
        raise AuthorNotFound(data.author_id)
    book_id = next_id(BOOKS)
    BOOKS[book_id] = {"id": book_id, **data.model_dump(), "cover": None}
    return BOOKS[book_id]


@router.patch("/{book_id}", response_model=BookOut)
def update_book(book: BookDep, changes: BookUpdate):
    update_data = changes.model_dump(exclude_unset=True)
    if "author_id" in update_data and update_data["author_id"] not in AUTHORS:
        raise AuthorNotFound(update_data["author_id"])
    book.update(update_data)
    return book


@router.post("/{book_id}/cover", response_model=BookOut)
async def upload_cover(book: BookDep, file: UploadFile):
    if file.content_type not in IMAGE_TYPES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Cover must be PNG or JPEG")
    filename = f"book_{book['id']}{IMAGE_TYPES[file.content_type]}"
    (UPLOAD_DIR / filename).write_bytes(await file.read())
    book["cover"] = filename
    return book
