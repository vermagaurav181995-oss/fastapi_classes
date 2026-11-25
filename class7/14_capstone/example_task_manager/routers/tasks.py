from datetime import date
from typing import Annotated

from fastapi import APIRouter, Query, status

from dependencies import PaginationDep
from permissions import ensure_owner, get_task_or_404, is_admin
from schemas import TaskOut, TaskStatus, TaskUpdate
from security import CurrentUser
from storage import TASKS

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskOut])
def list_tasks(
    user: CurrentUser,
    page: PaginationDep,
    status_filter: Annotated[TaskStatus | None, Query(alias="status")] = None,
    due_before: date | None = None,
    due_after: date | None = None,
    project_id: int | None = None,
):
    tasks = [t for t in TASKS.values() if is_admin(user) or t["owner_id"] == user["id"]]
    if status_filter is not None:
        tasks = [t for t in tasks if t["status"] == status_filter]
    if project_id is not None:
        tasks = [t for t in tasks if t["project_id"] == project_id]
    if due_before is not None:
        tasks = [t for t in tasks if t["due_date"] is not None and t["due_date"] <= due_before]
    if due_after is not None:
        tasks = [t for t in tasks if t["due_date"] is not None and t["due_date"] >= due_after]
    tasks.sort(key=lambda t: (t["due_date"] is None, t["due_date"] or date.max, t["id"]))
    return page.apply(tasks)


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, user: CurrentUser):
    task = get_task_or_404(task_id)
    ensure_owner(task, user, admin_allowed=True)
    return task


@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, changes: TaskUpdate, user: CurrentUser):
    task = get_task_or_404(task_id)
    ensure_owner(task, user, admin_allowed=False)
    task.update(changes.model_dump(exclude_unset=True))
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, user: CurrentUser) -> None:
    task = get_task_or_404(task_id)
    ensure_owner(task, user, admin_allowed=True)
    del TASKS[task_id]
