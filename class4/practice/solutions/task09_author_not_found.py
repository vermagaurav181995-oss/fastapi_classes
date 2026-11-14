from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Task 9 - solution")

AUTHORS = {1: "Frank Herbert", 2: "George Orwell"}


class AuthorNotFound(Exception):
    def __init__(self, author_id: int):
        self.author_id = author_id


@app.exception_handler(AuthorNotFound)
async def author_not_found_handler(request: Request, exc: AuthorNotFound):
    return JSONResponse(
        status_code=404,
        content={"error": "AuthorNotFound", "message": f"Author {exc.author_id} not found"},
    )


@app.get("/authors/{author_id}")
def get_author(author_id: int):
    if author_id not in AUTHORS:
        raise AuthorNotFound(author_id)
    return {"id": author_id, "name": AUTHORS[author_id]}
