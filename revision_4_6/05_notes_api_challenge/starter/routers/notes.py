from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Query, status

from schemas import NoteCreate, NoteUpdate
from security import CurrentUser

router = APIRouter(prefix="/notes", tags=["notes"])


class Pagination:
    def __init__(
        self,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=50)] = 10,
    ):
        raise NotImplementedError

    def apply(self, items: list) -> list:
        raise NotImplementedError


PaginationDep = Annotated[Pagination, Depends()]


def get_note_or_404(note_id: int) -> dict:
    raise NotImplementedError


def ensure_owner(note: dict, user: dict) -> None:
    raise NotImplementedError


def announce_note_created(note_id: int, email: str) -> None:
    raise NotImplementedError


@router.post("", status_code=status.HTTP_201_CREATED)
def create_note(data: NoteCreate, user: CurrentUser, background_tasks: BackgroundTasks):
    raise NotImplementedError


@router.get("")
def list_my_notes(user: CurrentUser, page: PaginationDep, q: str | None = None):
    raise NotImplementedError


@router.get("/{note_id}")
def get_note(note_id: int, user: CurrentUser):
    raise NotImplementedError


@router.patch("/{note_id}")
def update_note(note_id: int, changes: NoteUpdate, user: CurrentUser):
    raise NotImplementedError


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, user: CurrentUser) -> None:
    raise NotImplementedError
