from fastapi import APIRouter, Depends, status

from db import BOOKS
from dependencies import BookDep, verify_api_key

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(verify_api_key)])


@router.get("/stats")
def stats():
    return {
        "books": len(BOOKS),
        "units_in_stock": sum(b["stock"] for b in BOOKS.values()),
        "stock_cost_value": round(sum(b["stock"] * b["cost_price"] for b in BOOKS.values()), 2),
    }


@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book: BookDep) -> None:
    del BOOKS[book["id"]]
