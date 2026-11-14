from typing import Annotated

from fastapi import FastAPI, HTTPException, Path

app = FastAPI(title="02 - Path Validation")

ITEMS = {
    1: {"id": 1, "name": "Keyboard"},
    2: {"id": 2, "name": "Mouse"},
    3: {"id": 3, "name": "Monitor"},
}


@app.get("/items/{item_id}")
def get_item(
    item_id: Annotated[int, Path(ge=1, le=1000, description="ID of the item")],
):
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return ITEMS[item_id]


@app.get("/users/{username}")
def get_user(
    username: Annotated[
        str, Path(min_length=3, max_length=15, pattern=r"^[a-z0-9_]+$")
    ],
):
    return {"username": username}
