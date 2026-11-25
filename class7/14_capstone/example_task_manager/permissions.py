from fastapi import HTTPException, status

from exceptions import NotFoundError
from storage import PROJECTS, TASKS


def is_admin(user: dict) -> bool:
    return user["role"] == "admin"


def ensure_owner(resource: dict, user: dict, *, admin_allowed: bool) -> None:
    if resource["owner_id"] == user["id"] or (admin_allowed and is_admin(user)):
        return
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have access to this resource")


def get_project_or_404(project_id: int) -> dict:
    if project_id not in PROJECTS:
        raise NotFoundError("Project", project_id)
    return PROJECTS[project_id]


def get_task_or_404(task_id: int) -> dict:
    if task_id not in TASKS:
        raise NotFoundError("Task", task_id)
    return TASKS[task_id]
