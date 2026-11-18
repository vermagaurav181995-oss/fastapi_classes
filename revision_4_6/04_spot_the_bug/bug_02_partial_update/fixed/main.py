from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Bug 02 - partial update (fixed)")

ITEMS: dict[int, dict] = {
    1: {"id": 1, "name": "Pen", "price": 1.5, "in_stock": True},
    2: {"id": 2, "name": "Mug", "price": 8.0, "in_stock": False},
}


class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    in_stock: bool | None = None


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in ITEMS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return ITEMS[item_id]


@app.patch("/items/{item_id}")
def update_item(item_id: int, changes: ItemUpdate):
    item = get_item(item_id)
    item.update(changes.model_dump(exclude_unset=True))
    return item
