from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class NotFoundError(Exception):
    def __init__(self, resource: str, resource_id: int):
        self.resource = resource
        self.resource_id = resource_id


class BookNotFound(NotFoundError):
    def __init__(self, book_id: int):
        super().__init__("Book", book_id)


class AuthorNotFound(NotFoundError):
    def __init__(self, author_id: int):
        super().__init__("Author", author_id)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": type(exc).__name__,
                "message": f"{exc.resource} {exc.resource_id} not found",
            },
        )
