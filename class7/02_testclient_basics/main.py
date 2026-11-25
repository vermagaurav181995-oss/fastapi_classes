from typing import Annotated

from fastapi import Cookie, FastAPI, Form, Header, HTTPException, Path, Query, UploadFile, status
from pydantic import BaseModel, Field

app = FastAPI(title="02 - Bookstore for TestClient")

DEFAULT_BOOKS = [
    {"title": "Dune", "price": 9.99},
    {"title": "1984", "price": 7.5},
    {"title": "Neuromancer", "price": 8.25},
]
BOOKS: dict[int, dict] = {}


def seed_books() -> None:
    for book_id, book in enumerate(DEFAULT_BOOKS, start=1):
        BOOKS[book_id] = {"id": book_id, **book}


seed_books()


class BookIn(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    price: Annotated[float, Field(gt=0)]


@app.get("/books")
def list_books():
    return list(BOOKS.values())


@app.get("/books/{book_id}")
def get_book(book_id: Annotated[int, Path(ge=1)]):
    if book_id not in BOOKS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return BOOKS[book_id]


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: BookIn):
    book_id = max(BOOKS, default=0) + 1
    BOOKS[book_id] = {"id": book_id, **book.model_dump()}
    return BOOKS[book_id]


@app.get("/search")
def search(q: Annotated[str, Query(min_length=2)]):
    return {"q": q, "results": [b for b in BOOKS.values() if q.lower() in b["title"].lower()]}


@app.get("/client")
def client_info(x_client: Annotated[str, Header()]):
    return {"client": x_client}


@app.post("/login")
def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    if password != "secret":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")
    return {"message": f"Welcome {username}"}


@app.post("/upload")
async def upload(file: UploadFile):
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}


@app.get("/session")
def session(session_id: Annotated[str | None, Cookie()] = None):
    if session_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No session cookie")
    return {"session_id": session_id}
