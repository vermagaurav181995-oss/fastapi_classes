from collections import Counter

from fastapi import APIRouter

from schemas import UserOut
from security import AdminUser
from storage import PROJECTS, TASKS, USERS

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut])
def list_users(admin: AdminUser):
    return list(USERS.values())


@router.get("/stats")
def stats(admin: AdminUser):
    return {
        "users": len(USERS),
        "projects": len(PROJECTS),
        "tasks": len(TASKS),
        "tasks_by_status": dict(Counter(t["status"].value for t in TASKS.values())),
    }
