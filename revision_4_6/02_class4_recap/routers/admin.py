from fastapi import APIRouter, Depends

from dependencies import verify_api_key

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(verify_api_key)])

STATS = {"visits": 42, "orders": 7}


@router.get("/stats")
def read_stats():
    return STATS


@router.post("/stats/reset")
def reset_stats():
    STATS.update(visits=0, orders=0)
    return STATS
