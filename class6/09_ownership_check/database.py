"""
Database setup (SQLAlchemy 2.0, sync Session) - same pattern as Class 5.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from config import settings

# check_same_thread=False: SQLite only. FastAPI may use the session in another thread.
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    """One session per request, always closed afterwards (a yield dependency)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Type alias: write `db: DbSession` in any route to get a session
DbSession = Annotated[Session, Depends(get_db)]
