"""
15 - Bookstore API (everything from Class 6)
============================================
config.py      settings from .env (SECRET_KEY required)
database.py    engine, SessionLocal, get_db / DbSession
models.py      User, Author, Book, Review
schemas.py     request / response models (no passwords out!)
security.py    hashing, JWT, get_current_user, require_role
exceptions.py  NotFoundError / ConflictError + JSON handlers
routers/       auth, authors, books, reviews
main.py        lifespan, CORS, logging middleware, routers   <- you are here

Setup:  cp .env.example .env
Run:    fastapi dev main.py         Docs: http://127.0.0.1:8000/docs
"""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from config import settings
from database import Base, SessionLocal, engine
from exceptions import register_exception_handlers
from models import Author, Book, User
from routers import auth, authors, books, reviews
from security import hash_password


def seed() -> None:
    """First admin from .env + a few books, only when they don't exist yet."""
    with SessionLocal() as db:
        no_admin = db.scalar(select(User).where(User.role == "admin")) is None
        if no_admin and settings.admin_email and settings.admin_password:
            db.add(User(email=settings.admin_email, hashed_password=hash_password(settings.admin_password), role="admin"))
            print(f"[startup] created admin {settings.admin_email}")
        if db.scalar(select(Author)) is None:
            db.add(Author(name="Frank Herbert", books=[Book(title="Dune", year=1965)]))
            db.add(Author(name="George Orwell", books=[Book(title="1984", year=1949), Book(title="Animal Farm", year=1945)]))
        db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)  # STARTUP
    seed()
    yield
    engine.dispose()  # SHUTDOWN


app = FastAPI(title="15 - Bookstore API", version="1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time-ms"] = f"{ms:.2f}"
    print(f"{request.method} {request.url.path} -> {response.status_code} ({ms:.2f} ms)")
    return response


register_exception_handlers(app)
for router in (auth.router, authors.router, books.router, reviews.router):
    app.include_router(router)


@app.get("/", tags=["root"])
def root():
    return {"message": "Bookstore API. Open /docs and click Authorize to log in."}


# ---------------------------------------------------------------------------
# TRY IT  (full endpoint list in README.md)
# ---------------------------------------------------------------------------
# GET    /books                        -> 200 [Dune, 1984, Animal Farm]   (public)
# POST   /auth/register {"email": "ada@example.com", "password": "supersecret"} -> 201
# POST   /auth/login FORM username=ada@example.com&password=supersecret       -> 200 {token}
# POST   /books {"title": "Emma", "year": 1815, "author_id": 1} + token        -> 201
# POST   /books/1/reviews {"rating": 5, "text": "Great"} + token               -> 201
# DELETE /books/3  + adminToken (admin@example.com / admin12345)               -> 204
#
# These should FAIL:
# POST   /auth/register (same email again)   -> 409 {"error": "Conflict", ...}
# POST   /books (no token)                   -> 401 "Not authenticated"
# DELETE /books/1 + ada's token              -> 403 "Not enough permissions"
# PATCH  /reviews/<someone else's> + token   -> 403 "You can only change your own reviews"
# GET    /books/999                          -> 404 {"error": "NotFound", "message": "Book 999 not found"}
# POST   /books {"title": "", ...} + token   -> 422
