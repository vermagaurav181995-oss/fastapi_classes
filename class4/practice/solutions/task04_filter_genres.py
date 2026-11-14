from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI(title="Task 4 - solution")


@app.get("/filter")
def filter_genres(genre: Annotated[list[str], Query(min_length=1)]):
    return {"genres": genre}
