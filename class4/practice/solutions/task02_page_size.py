from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI(title="Task 2 - solution")

NUMBERS = list(range(1, 101))


@app.get("/numbers")
def numbers(page_size: Annotated[int, Query(ge=1, le=50)] = 10):
    return {"page_size": page_size, "items": NUMBERS[:page_size]}
