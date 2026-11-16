"""
Task 2 - The User model
Create a SQLAlchemy 2.0 model with:
    id (primary key), email (unique, indexed, max 255), hashed_password,
    role (default "user"), is_active (default True)
Run:  fastapi dev task02_user_model.py      Check: GET /columns lists all 5 columns
"""

from fastapi import FastAPI
from sqlalchemy import String  # noqa: F401  (you'll need it)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from common import engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "task02_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: email      -> Mapped[str], String(255), unique=True, index=True
    # TODO: hashed_password -> Mapped[str]
    # TODO: role       -> Mapped[str], default "user"
    # TODO: is_active  -> Mapped[bool], default True


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Task 2 - User model")


@app.get("/columns")
def columns():
    return {c.name: {"type": str(c.type), "unique": bool(c.unique)} for c in User.__table__.columns}
