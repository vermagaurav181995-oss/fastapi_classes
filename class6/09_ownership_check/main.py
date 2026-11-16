"""
09 - Ownership checks
=====================
Roles answer "what KIND of user are you?". Ownership answers "is this YOURS?".
routers/reviews.py -> get_review_for_change(): owner or admin, else 403.

Setup:  cp .env.example .env
Run:    fastapi dev main.py         Docs: http://127.0.0.1:8000/docs
Demo users (created on startup):
    admin@example.com / admin12345  (admin)
    alice@example.com / alice12345  (user, owns review 1)
    bob@example.com   / bob1234567  (user, owns review 2)
"""

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
            return  # already seeded
        users = [User(email=e, hashed_password=hash_password(p), role=r) for e, p, r in DEMO_USERS]
        db.add_all(users)
        db.flush()  # assigns ids without committing yet
        db.add_all([
            Review(book_title="Dune", text="A classic!", rating=5, owner_id=users[1].id),  # alice
            Review(book_title="1984", text="Scary.", rating=4, owner_id=users[2].id),  # bob
        ])
        db.commit()


Base.metadata.create_all(bind=engine)
seed()

app = FastAPI(title="09 - Ownership")
app.include_router(auth.router)
app.include_router(reviews.router)


# ---------------------------------------------------------------------------
# TRY IT  (log in as alice, bob and admin to get three tokens)
# ---------------------------------------------------------------------------
# GET    /reviews                                   -> 200 (public)
# POST   /reviews {"book_title": "Emma", "text": "Lovely", "rating": 4} + aliceToken -> 201
# PATCH  /reviews/1 {"rating": 3}     + aliceToken  -> 200 (alice owns review 1)
# PATCH  /reviews/2 {"text": "Edited by admin"} + adminToken -> 200 (admins may edit any)
# DELETE /reviews/1                   + aliceToken  -> 204
#
# These should FAIL:
# PATCH  /reviews/2 {"rating": 1}     + aliceToken  -> 403 "You can only change your own reviews"
# DELETE /reviews/2                   + aliceToken  -> 403
# PATCH  /reviews/2                   (no token)    -> 401 "Not authenticated"
# POST   /reviews {... "rating": 9}   + aliceToken  -> 422 (rating must be 1-5)
