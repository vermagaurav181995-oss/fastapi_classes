from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

app = FastAPI(title="08 - Custom Exceptions")


class BookNotFound(Exception):
    def __init__(self, book_id: int):
        self.book_id = book_id


class OutOfStock(Exception):
    def __init__(self, title: str):
        self.title = title


@app.exception_handler(BookNotFound)
async def book_not_found_handler(request: Request, exc: BookNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "BookNotFound", "message": f"Book {exc.book_id} does not exist"},
    )


@app.exception_handler(OutOfStock)
async def out_of_stock_handler(request: Request, exc: OutOfStock):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": "OutOfStock", "message": f"'{exc.title}' is sold out"},
    )


BOOKS = {
    1: {"id": 1, "title": "Dune", "stock": 2},
    2: {"id": 2, "title": "1984", "stock": 0},
}


def find_book(book_id: int) -> dict:
    if book_id not in BOOKS:
        raise BookNotFound(book_id)
    return BOOKS[book_id]


@app.get("/books/{book_id}")
def get_book(book_id: int):
    return find_book(book_id)


@app.post("/books/{book_id}/buy")
def buy_book(book_id: int):
    book = find_book(book_id)
    if book["stock"] == 0:
        raise OutOfStock(book["title"])
    book["stock"] -= 1
    return {"message": f"You bought '{book['title']}'", "stock_left": book["stock"]}
