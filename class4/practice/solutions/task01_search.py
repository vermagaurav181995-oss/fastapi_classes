from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI(title="Task 1 - solution")

FRUITS = ["apple", "apricot", "banana", "blueberry", "cherry"]


@app.get("/search")
def search(q: Annotated[str, Query(min_length=2, max_length=20)]):
    return {"q": q, "results": [f for f in FRUITS if q.lower() in f]}
