from fastapi import APIRouter, Depends

from dependencies import verify_api_key

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(verify_api_key)],
)

STATS = {"users": 42, "orders": 7}


@router.get("/stats")
def get_stats():
    return STATS


@router.post("/reset")
def reset_stats():
    STATS.update(users=0, orders=0)
    return {"message": "Stats reset", "stats": STATS}
