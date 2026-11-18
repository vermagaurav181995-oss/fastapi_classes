from fastapi import FastAPI


class NoteNotFound(Exception):
    def __init__(self, note_id: int):
        raise NotImplementedError


def register_exception_handlers(app: FastAPI) -> None:
    raise NotImplementedError
