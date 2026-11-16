"""Solution 2: the User model."""

from fastapi import FastAPI
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from common import engine


class Base(DeclarativeBase):  # own Base so this task doesn't clash with common.User
    pass


class User(Base):
    __tablename__ = "task02_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str]
    role: Mapped[str] = mapped_column(String(20), default="user")
    is_active: Mapped[bool] = mapped_column(default=True)


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Task 2 - solution")


@app.get("/columns")
def columns():
    return {c.name: {"type": str(c.type), "unique": bool(c.unique)} for c in User.__table__.columns}

# GET /columns -> id, email (unique), hashed_password, role, is_active
