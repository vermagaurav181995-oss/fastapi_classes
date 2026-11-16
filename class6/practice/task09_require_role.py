"""
Task 9 - require_role
Write a dependency FACTORY require_role(*roles) and make DELETE /books/{id} admin-only.
Users: student@example.com / password123 (user) -> 403
       admin@example.com   / admin12345  (admin) -> 204
Run:  fastapi dev task09_require_role.py
"""

from fastapi import FastAPI, HTTPException, status

from common import CurrentUser, User, login_router, seed_demo_users  # noqa: F401

seed_demo_users()
app = FastAPI(title="Task 9 - roles")
app.include_router(login_router)

BOOKS = {1: "Dune", 2: "1984", 3: "Emma"}


def require_role(*roles: str):
    # TODO: define an inner checker(user: CurrentUser) that raises 403 if user.role not in roles
    # TODO: return checker
    pass


# TODO: AdminUser = Annotated[User, Depends(require_role("admin"))]


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int) -> None:  # TODO: add  admin: AdminUser
    if BOOKS.pop(book_id, None) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
