from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Path, status

from exceptions import BookNotFound
from security import AdminUser
from storage import BOOKS, DELETION_LOG

router = APIRouter(prefix="/books", tags=["books"])

BookId = Annotated[int, Path(ge=1)]


def get_book_store():
    print("[store] setup: book store opened")
    try:
        yield BOOKS
    finally:
        print("[store] cleanup: book store closed")


BookStore = Annotated[dict[int, dict], Depends(get_book_store)]


def record_deletion(title: str) -> None:
    DELETION_LOG.append(title)
    print(f"[background] deletion of '{title}' recorded")


@router.get("")
def list_books(store: BookStore):
    return list(store.values())


@router.get("/{book_id}")
def get_book(book_id: BookId, store: BookStore):
    if book_id not in store:
        raise BookNotFound(book_id)
    return store[book_id]


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: BookId, admin: AdminUser, store: BookStore, background_tasks: BackgroundTasks) -> None:
    print(f"[route] {admin['email']} deletes book {book_id}")
    if book_id not in store:
        raise BookNotFound(book_id)
    book = store.pop(book_id)
    background_tasks.add_task(record_deletion, book["title"])


@router.get("/admin/deletions")
def list_deletions(admin: AdminUser):
    return DELETION_LOG
