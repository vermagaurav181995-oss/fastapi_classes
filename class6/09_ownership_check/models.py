"""SQLAlchemy models = database tables."""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str]  # NEVER store the plain password
    role: Mapped[str] = mapped_column(String(20), default="user")  # "user" or "admin"
    is_active: Mapped[bool] = mapped_column(default=True)


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_title: Mapped[str] = mapped_column(String(200))
    text: Mapped[str] = mapped_column(String(1000))
    rating: Mapped[int]
    # Who wrote it -> used for the ownership check
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
