from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status

from exceptions import NoteNotFound
from schemas import NoteCreate, NoteOut, NoteUpdate
from security import CurrentUser, get_current_user
from storage import NOTE_EVENTS, NOTES, add_note

router = APIRouter(prefix="/notes", tags=["notes"], dependencies=[Depends(get_current_user)])


class Pagination:
    def __init__(
        self,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=50)] = 10,
    ):
        self.skip = skip
        self.limit = limit

    def apply(self, items: list) -> list:
        return items[self.skip : self.skip + self.limit]


PaginationDep = Annotated[Pagination, Depends()]


def get_note_or_404(note_id: int) -> dict:
    if note_id not in NOTES:
        raise NoteNotFound(note_id)
    return NOTES[note_id]


def ensure_owner(note: dict, user: dict) -> None:
    if note["owner_id"] != user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This note belongs to someone else")


def announce_note_created(note_id: int, email: str) -> None:
    NOTE_EVENTS.append(f"note {note_id} created by {email}")
    print(f"[background] note {note_id} created by {email}")


@router.post("", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(data: NoteCreate, user: CurrentUser, background_tasks: BackgroundTasks):
    note = add_note(data.title, data.content, owner_id=user["id"])
    background_tasks.add_task(announce_note_created, note["id"], user["email"])
    return note


@router.get("", response_model=list[NoteOut])
def list_my_notes(
    user: CurrentUser,
    page: PaginationDep,
    q: Annotated[str | None, Query(min_length=2)] = None,
):
    notes = [note for note in NOTES.values() if note["owner_id"] == user["id"]]
    if q:
        needle = q.lower()
        notes = [note for note in notes if needle in note["title"].lower() or needle in note["content"].lower()]
    return page.apply(notes)


@router.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: int, user: CurrentUser):
    note = get_note_or_404(note_id)
    ensure_owner(note, user)
    return note


@router.patch("/{note_id}", response_model=NoteOut)
def update_note(note_id: int, changes: NoteUpdate, user: CurrentUser):
    note = get_note_or_404(note_id)
    ensure_owner(note, user)
    note.update(changes.model_dump(exclude_unset=True))
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, user: CurrentUser) -> None:
    note = get_note_or_404(note_id)
    if user["role"] != "admin":
        ensure_owner(note, user)
    del NOTES[note_id]
