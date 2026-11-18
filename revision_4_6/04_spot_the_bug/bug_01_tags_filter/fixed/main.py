from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI(title="Bug 01 - tags filter (fixed)")

PRODUCTS = [
    {"name": "laptop", "tags": ["tech", "work"]},
    {"name": "headphones", "tags": ["tech", "music"]},
    {"name": "notebook", "tags": ["work", "school"]},
    {"name": "guitar", "tags": ["music"]},
]


@app.get("/filter")
def filter_by_tags(tag: Annotated[list[str] | None, Query()] = None):
    if not tag:
        return {"tags": [], "results": PRODUCTS}
    return {"tags": tag, "results": [p for p in PRODUCTS if set(tag) & set(p["tags"])]}
