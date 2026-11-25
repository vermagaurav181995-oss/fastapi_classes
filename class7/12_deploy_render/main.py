from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, status
from fastapi.middleware.cors import CORSMiddleware

from config import settings

app = FastAPI(
    title="12 - Deploy-ready Bookstore",
    docs_url=None if settings.is_production else "/docs",
    redoc_url=None if settings.is_production else "/redoc",
    openapi_url=None if settings.is_production else "/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOOKS = {1: {"id": 1, "title": "Dune"}, 2: {"id": 2, "title": "1984"}}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Bookstore API is running", "environment": settings.environment}


@app.get("/books")
def list_books():
    return list(BOOKS.values())


@app.get("/books/{book_id}")
def get_book(book_id: Annotated[int, Path(ge=1)]):
    if book_id not in BOOKS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return BOOKS[book_id]
