from fastapi import FastAPI, HTTPException, status

from common import CurrentUser, User, login_router, seed_demo_users

seed_demo_users()
app = FastAPI(title="Task 9 - roles")
app.include_router(login_router)

BOOKS = {1: "Dune", 2: "1984", 3: "Emma"}


def require_role(*roles: str):
    pass


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int) -> None:
    if BOOKS.pop(book_id, None) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
