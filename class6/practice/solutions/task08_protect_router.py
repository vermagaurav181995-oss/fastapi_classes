"""Solution 8: protect the whole books router."""

from fastapi import APIRouter, Depends, FastAPI

from common import get_current_user, login_router, seed_demo_users

seed_demo_users()

books = APIRouter(prefix="/books", tags=["books"], dependencies=[Depends(get_current_user)])


@books.get("")
def list_books():
    return ["Dune", "1984"]


@books.get("/count")
def count_books():
    return {"count": 2}


app = FastAPI(title="Task 8 - solution")
app.include_router(login_router)
app.include_router(books)

# GET /books without token -> 401     with token -> 200
