from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI(title="01 - Query Validation")

PRODUCTS = [
    {"name": "laptop", "tags": ["tech", "work"]},
    {"name": "headphones", "tags": ["tech", "music"]},
    {"name": "notebook", "tags": ["work", "school"]},
    {"name": "guitar", "tags": ["music"]},
]


@app.get("/search")
def search(
    q: Annotated[str | None, Query(min_length=2, max_length=20)] = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
):
    results = PRODUCTS
    if q:
        results = [p for p in PRODUCTS if q.lower() in p["name"]]
    return {"q": q, "limit": limit, "results": results[:limit]}


@app.get("/greet")
def greet(
    name: Annotated[str, Query(min_length=1, max_length=30)],
):
    return {"message": f"Hello, {name}!"}


@app.get("/filter")
def filter_by_tags(
    tag: Annotated[list[str] | None, Query()] = None,
):
    if not tag:
        return {"tags": [], "results": PRODUCTS}
    results = [p for p in PRODUCTS if set(tag) & set(p["tags"])]
    return {"tags": tag, "results": results}
