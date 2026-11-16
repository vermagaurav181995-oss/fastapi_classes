"""
Task 8 - Protect the whole books router
Every /books route must need a valid token, without adding a parameter to each route.
Run:  fastapi dev task08_protect_router.py
Check: GET /books without a token -> 401, with a token -> 200
"""

from fastapi import APIRouter, Depends, FastAPI  # noqa: F401

from common import get_current_user, login_router, seed_demo_users  # noqa: F401

seed_demo_users()

books = APIRouter(prefix="/books", tags=["books"])  # TODO: dependencies=[Depends(...)]


@books.get("")
def list_books():
    return ["Dune", "1984"]


@books.get("/count")
def count_books():
    return {"count": 2}


app = FastAPI(title="Task 8 - protect router")
app.include_router(login_router)
app.include_router(books)
