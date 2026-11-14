from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI(title="Task 1 - /search")

FRUITS = ["apple", "apricot", "banana", "blueberry", "cherry"]


@app.get("/search")
def search(q: str):
    return {"todo": "implement me"}
