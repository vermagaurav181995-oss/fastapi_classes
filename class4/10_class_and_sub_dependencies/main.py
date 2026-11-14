from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status

app = FastAPI(title="10 - Class & Sub-dependencies")


class Pagination:
    def __init__(
        self,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=50)] = 3,
    ):
        self.skip = skip
        self.limit = limit

    def apply(self, items: list) -> list:
        return items[self.skip : self.skip + self.limit]


PaginationDep = Annotated[Pagination, Depends()]

TOKENS = {"alice-token": "alice", "bob-token": "bob"}
USERS = {"alice": {"username": "alice", "role": "admin"}, "bob": {"username": "bob", "role": "reader"}}


def get_token(x_token: Annotated[str | None, Header()] = None) -> str:
    if x_token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Missing X-Token header")
    return x_token


def get_current_user(token: Annotated[str, Depends(get_token)]) -> dict:
    if token not in TOKENS:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return USERS[TOKENS[token]]


CurrentUser = Annotated[dict, Depends(get_current_user)]

PRODUCTS = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]


@app.get("/products")
def list_products(page: PaginationDep):
    return {"skip": page.skip, "limit": page.limit, "items": page.apply(PRODUCTS)}


@app.get("/me")
def read_me(user: CurrentUser):
    return user


@app.get("/my-products")
def my_products(user: CurrentUser, page: PaginationDep):
    return {"user": user["username"], "items": page.apply(PRODUCTS)}
