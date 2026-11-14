from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI(title="Task 2 - page_size")

NUMBERS = list(range(1, 101))


@app.get("/numbers")
def numbers(page_size: int = 10):
    return {"todo": "implement me"}
