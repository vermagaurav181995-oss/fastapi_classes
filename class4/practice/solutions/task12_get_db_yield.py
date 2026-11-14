from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI(title="Task 12 - solution")


def get_db():
    db = {1: "Dune", 2: "1984"}
    print("DB OPEN")
    try:
        yield db
    finally:
        print("DB CLOSE")


@app.get("/books/{book_id}")
def get_book(book_id: int, db: Annotated[dict, Depends(get_db)]):
    if book_id not in db:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"id": book_id, "title": db[book_id]}
