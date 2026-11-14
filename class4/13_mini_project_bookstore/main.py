from fastapi import FastAPI

from exceptions import register_exception_handlers
from routers import admin, authors, books

app = FastAPI(title="13 - Bookstore API", version="1.0")

register_exception_handlers(app)
app.include_router(books.router)
app.include_router(authors.router)
app.include_router(admin.router)


@app.get("/", tags=["root"])
def root():
    return {"message": "Welcome to the Bookstore API. Open /docs to explore."}
