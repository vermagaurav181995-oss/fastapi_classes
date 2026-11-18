from fastapi import APIRouter

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/info")
def info():
    return {"shop": "Class 6 Bookstore", "open": True}


@router.get("/bestsellers")
def bestsellers():
    return ["Dune", "1984"]
