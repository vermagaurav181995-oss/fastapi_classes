from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, status

app = FastAPI(title="Bug 07 - admin check (buggy)")

TOKENS = {
    "admin-token": {"username": "grace", "role": "admin"},
    "user-token": {"username": "linus", "role": "user"},
}
BOOKS = {1: "Dune", 2: "1984", 3: "Emma"}


def get_current_user(x_token: Annotated[str | None, Header()] = None) -> dict:
    if x_token not in TOKENS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")
    return TOKENS[x_token]


def require_admin(user: Annotated[dict, Depends(get_current_user)]) -> dict:
    if user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admins only")
    return user


@app.get("/books")
def list_books(user: Annotated[dict, Depends(get_current_user)]):
    return BOOKS


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, admin: Annotated[dict, Depends(require_admin)]) -> None:
    if BOOKS.pop(book_id, None) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
