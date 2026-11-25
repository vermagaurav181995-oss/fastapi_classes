from fastapi import APIRouter, status

from dependencies import PaginationDep
from permissions import ensure_owner, get_project_or_404, is_admin
from schemas import ProjectCreate, ProjectOut, ProjectUpdate, TaskCreate, TaskOut
from security import CurrentUser
from storage import PROJECTS, TASKS, next_id

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectCreate, user: CurrentUser):
    project_id = next_id(PROJECTS)
    PROJECTS[project_id] = {"id": project_id, **data.model_dump(), "owner_id": user["id"]}
    return PROJECTS[project_id]


@router.get("", response_model=list[ProjectOut])
def list_projects(user: CurrentUser, page: PaginationDep):
    projects = [p for p in PROJECTS.values() if is_admin(user) or p["owner_id"] == user["id"]]
    return page.apply(projects)


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, user: CurrentUser):
    project = get_project_or_404(project_id)
    ensure_owner(project, user, admin_allowed=True)
    return project


@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, changes: ProjectUpdate, user: CurrentUser):
    project = get_project_or_404(project_id)
    ensure_owner(project, user, admin_allowed=False)
    project.update(changes.model_dump(exclude_unset=True))
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, user: CurrentUser) -> None:
    project = get_project_or_404(project_id)
    ensure_owner(project, user, admin_allowed=True)
    for task_id in [t["id"] for t in TASKS.values() if t["project_id"] == project_id]:
        del TASKS[task_id]
    del PROJECTS[project_id]


@router.post("/{project_id}/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(project_id: int, data: TaskCreate, user: CurrentUser):
    project = get_project_or_404(project_id)
    ensure_owner(project, user, admin_allowed=False)
    task_id = next_id(TASKS)
    TASKS[task_id] = {"id": task_id, "project_id": project_id, **data.model_dump(), "owner_id": user["id"]}
    return TASKS[task_id]


@router.get("/{project_id}/tasks", response_model=list[TaskOut])
def list_project_tasks(project_id: int, user: CurrentUser, page: PaginationDep):
    project = get_project_or_404(project_id)
    ensure_owner(project, user, admin_allowed=True)
    return page.apply([t for t in TASKS.values() if t["project_id"] == project_id])
