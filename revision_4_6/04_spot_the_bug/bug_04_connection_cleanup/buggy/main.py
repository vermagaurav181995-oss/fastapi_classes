from itertools import count
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI(title="Bug 04 - connection cleanup (buggy)")

BOOKS = ["Dune", "1984", "Neuromancer"]
OPEN_CONNECTIONS: set[int] = set()
connection_ids = count(1)


class FakeConnection:
    def __init__(self):
        self.id = next(connection_ids)
        OPEN_CONNECTIONS.add(self.id)
        print(f"[connection {self.id}] opened")

    def close(self) -> None:
        OPEN_CONNECTIONS.discard(self.id)
        print(f"[connection {self.id}] closed")


def get_connection():
    connection = FakeConnection()
    return connection

Connection = Annotated[FakeConnection, Depends(get_connection)]


@app.get("/books")
def list_books(connection: Connection):
    return {"connection_id": connection.id, "books": BOOKS}


@app.get("/health")
def health():
    return {"open_connections": len(OPEN_CONNECTIONS)}
