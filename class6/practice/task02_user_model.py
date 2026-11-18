from fastapi import FastAPI
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from common import engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "task02_users"

    id: Mapped[int] = mapped_column(primary_key=True)


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Task 2 - User model")


@app.get("/columns")
def columns():
    return {c.name: {"type": str(c.type), "unique": bool(c.unique)} for c in User.__table__.columns}
