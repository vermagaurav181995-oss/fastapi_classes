from fastapi import APIRouter

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/hello")
def hello():
    return {"message": "Hello, anyone can see this!"}


@router.get("/books")
def books():
    return ["Dune", "1984", "Neuromancer"]
