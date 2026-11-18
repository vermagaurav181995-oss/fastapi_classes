from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class NoteNotFound(Exception):
    def __init__(self, note_id: int):
        self.note_id = note_id


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NoteNotFound)
    async def note_not_found_handler(request: Request, exc: NoteNotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "NoteNotFound", "message": f"Note {exc.note_id} does not exist"},
        )
