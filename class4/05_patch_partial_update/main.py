from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="05 - PUT vs PATCH")


class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True


class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    in_stock: bool | None = None


ITEMS: dict[int, Item] = {
    1: Item(name="Pen", price=1.5),
    2: Item(name="Mug", price=8.0, in_stock=False),
}


def get_or_404(item_id: int) -> Item:
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return ITEMS[item_id]


@app.get("/items/{item_id}")
def read_item(item_id: int) -> Item:
    return get_or_404(item_id)


@app.put("/items/{item_id}")
def replace_item(item_id: int, item: Item) -> Item:
    get_or_404(item_id)
    ITEMS[item_id] = item
    return item


@app.patch("/items/{item_id}")
def update_item(item_id: int, changes: ItemUpdate) -> Item:
    stored = get_or_404(item_id)
    update_data = changes.model_dump(exclude_unset=True)
    updated = stored.model_copy(update=update_data)
    ITEMS[item_id] = updated
    return updated


@app.patch("/items/{item_id}/broken")
def broken_update(item_id: int, changes: ItemUpdate) -> dict:
    stored = get_or_404(item_id)
    update_data = changes.model_dump()
    return {
        "client_sent": changes.model_dump(exclude_unset=True),
        "model_dump_without_exclude_unset": update_data,
        "item_would_become": {**stored.model_dump(), **update_data},
    }
