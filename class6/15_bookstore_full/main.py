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
    Base.metadata.create_all(bind=engine)
    seed()
    yield
    engine.dispose()


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
