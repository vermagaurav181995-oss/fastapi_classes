from fastapi import FastAPI
from sqlalchemy import select

from database import Base, SessionLocal, engine
from models import Review, User
from routers import auth, reviews
from security import hash_password

DEMO_USERS = [
    ("admin@example.com", "admin12345", "admin"),
    ("alice@example.com", "alice12345", "user"),
    ("bob@example.com", "bob1234567", "user"),
]


def seed() -> None:
    with SessionLocal() as db:
        if db.scalar(select(User)) is not None:
            return
        users = [User(email=e, hashed_password=hash_password(p), role=r) for e, p, r in DEMO_USERS]
        db.add_all(users)
        db.flush()
        db.add_all([
            Review(book_title="Dune", text="A classic!", rating=5, owner_id=users[1].id),
            Review(book_title="1984", text="Scary.", rating=4, owner_id=users[2].id),
        ])
        db.commit()


Base.metadata.create_all(bind=engine)
seed()

app = FastAPI(title="09 - Ownership")
app.include_router(auth.router)
app.include_router(reviews.router)
