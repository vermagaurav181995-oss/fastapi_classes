from datetime import date
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]


class UserOut(BaseModel):
    id: int
    email: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProjectCreate(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    description: Annotated[str, Field(max_length=1000)] = ""


class ProjectUpdate(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    description: Annotated[str, Field(max_length=1000)] | None = None


class ProjectOut(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int


class TaskStatus(StrEnum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskCreate(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    description: Annotated[str, Field(max_length=2000)] = ""
    status: TaskStatus = TaskStatus.todo
    due_date: date | None = None


class TaskUpdate(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)] | None = None
    description: Annotated[str, Field(max_length=2000)] | None = None
    status: TaskStatus | None = None
    due_date: date | None = None


class TaskOut(BaseModel):
    id: int
    project_id: int
    title: str
    description: str
    status: TaskStatus
    due_date: date | None
    owner_id: int
