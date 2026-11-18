from fastapi import FastAPI
from sqlalchemy import select

from database import Base, SessionLocal, engine
from models import Book, User
from routers import auth, books
from security import hash_password

DEMO_USERS = [("admin@example.com", "admin12345", "admin"), ("user@example.com", "user12345", "user")]


def seed() -> None:
    with SessionLocal() as db:
        for email, password, role in DEMO_USERS:
            if db.scalar(select(User).where(User.email == email)) is None:
                db.add(User(email=email, hashed_password=hash_password(password), role=role))
        if db.scalar(select(Book)) is None:
            db.add_all([Book(title="Dune"), Book(title="1984"), Book(title="Neuromancer")])
        db.commit()


Base.metadata.create_all(bind=engine)
seed()

app = FastAPI(title="08 - Roles")
app.include_router(auth.router)
app.include_router(books.router)
