from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status

from common import CurrentUser, User, login_router, seed_demo_users

seed_demo_users()
app = FastAPI(title="Task 9 - solution")
app.include_router(login_router)

BOOKS = {1: "Dune", 2: "1984", 3: "Emma"}


def require_role(*roles: str):
    def checker(user: CurrentUser) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return user

    return checker


AdminUser = Annotated[User, Depends(require_role("admin"))]


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, admin: AdminUser) -> None:
    if BOOKS.pop(book_id, None) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
