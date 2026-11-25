from fastapi import APIRouter, HTTPException, status

from dependencies import PaginationDep
from schemas import ItemCreate, ItemOut, ItemUpdate
from security import CurrentUser

router = APIRouter(prefix="/items", tags=["items"])

NOT_IMPLEMENTED = HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="TODO: implement this route")


def get_item_or_404(item_id: int) -> dict:
    raise NOT_IMPLEMENTED


def ensure_can_change(item: dict, user: dict) -> None:
    raise NOT_IMPLEMENTED


@router.get("", response_model=list[ItemOut])
def list_my_items(user: CurrentUser, page: PaginationDep):
    raise NOT_IMPLEMENTED


@router.post("", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item(data: ItemCreate, user: CurrentUser):
    raise NOT_IMPLEMENTED


@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int, user: CurrentUser):
    raise NOT_IMPLEMENTED


@router.patch("/{item_id}", response_model=ItemOut)
def update_item(item_id: int, changes: ItemUpdate, user: CurrentUser):
    raise NOT_IMPLEMENTED


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, user: CurrentUser) -> None:
    raise NOT_IMPLEMENTED
