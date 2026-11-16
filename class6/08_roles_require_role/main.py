"""
08 - Roles with a dependency factory: require_role(*roles)
==========================================================
security.py:
    def require_role(*roles):         # a function that BUILDS a dependency
        def checker(user: CurrentUser):
            if user.role not in roles: raise 403
            return user
        return checker
    AdminUser = Annotated[User, Depends(require_role("admin"))]

401 = "who are you?" (no/bad token)     403 = "I know you, but you're not allowed"

Setup:  cp .env.example .env
Run:    fastapi dev main.py         Docs: http://127.0.0.1:8000/docs
Demo users (created on startup):  admin@example.com / admin12345  (admin)
                                  user@example.com  / user12345   (user)
"""

from fastapi import FastAPI
from sqlalchemy import select

from database import Base, SessionLocal, engine
from models import Book, User
from routers import auth, books
from security import hash_password

DEMO_USERS = [("admin@example.com", "admin12345", "admin"), ("user@example.com", "user12345", "user")]


def seed() -> None:
    """Create the demo users and books once (skips anything that already exists)."""
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


# ---------------------------------------------------------------------------
# TRY IT
# ---------------------------------------------------------------------------
# GET    /books                                -> 200 (public)
# POST   /auth/login FORM username=user@example.com&password=user12345   -> userToken
# POST   /auth/login FORM username=admin@example.com&password=admin12345 -> adminToken
# POST   /books {"title": "Emma"}   + userToken  -> 201
# DELETE /books/1                   + adminToken -> 204 (empty body)
#
# These should FAIL:
# DELETE /books/2                   + userToken  -> 403 "Not enough permissions"
# DELETE /books/2                   (no token)   -> 401 "Not authenticated"
# DELETE /books/999                 + adminToken -> 404 "Book not found"
# POST   /books {"title": ""}       + userToken  -> 422
