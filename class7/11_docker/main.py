import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import auth, books
from security import hash_password
from storage import add_user, find_user_by_email


def seed_admin() -> None:
    if settings.admin_email and settings.admin_password and not find_user_by_email(settings.admin_email):
        add_user(settings.admin_email, hash_password(settings.admin_password), role="admin")


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_admin()
    yield


app = FastAPI(title="11 - Bookstore in Docker", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time-ms"] = f"{(time.perf_counter() - start) * 1000:.2f}"
    return response


app.include_router(auth.router)
app.include_router(books.router)


@app.get("/")
def root():
    return {"message": "Bookstore API. Open /docs"}
