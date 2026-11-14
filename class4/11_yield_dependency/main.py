from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI(title="11 - yield Dependencies")


class FakeDB:
    def __init__(self):
        self.books = {1: "Dune", 2: "1984"}


def get_db():
    db = FakeDB()
    print("[get_db] 1. OPEN connection")
    try:
        yield db
    except Exception:
        print("[get_db] !  route raised an error -> ROLLBACK")
        raise
    finally:
        print("[get_db] 3. CLOSE connection")


DbDep = Annotated[FakeDB, Depends(get_db)]


@app.get("/books")
def list_books(db: DbDep):
    print("[route ] 2. route running")
    return db.books


@app.get("/books/{book_id}")
def get_book(book_id: int, db: DbDep):
    print("[route ] 2. route running")
    if book_id not in db.books:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"id": book_id, "title": db.books[book_id]}
