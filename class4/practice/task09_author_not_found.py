from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Task 9 - custom exception")

AUTHORS = {1: "Frank Herbert", 2: "George Orwell"}


class AuthorNotFound(Exception):
    pass


@app.get("/authors/{author_id}")
def get_author(author_id: int):
    return {"id": author_id, "name": AUTHORS.get(author_id)}
