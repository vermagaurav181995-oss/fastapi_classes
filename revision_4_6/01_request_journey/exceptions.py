from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class BookNotFound(Exception):
    def __init__(self, book_id: int):
        self.book_id = book_id


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(BookNotFound)
    async def book_not_found_handler(request: Request, exc: BookNotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "BookNotFound", "message": f"Book {exc.book_id} does not exist"},
        )
