import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from exceptions import register_exception_handlers
from routers import auth, notes
from security import hash_password
from storage import USERS, add_user


def seed_admin() -> None:
    has_admin = any(user["role"] == "admin" for user in USERS.values())
    if not has_admin and settings.admin_email and settings.admin_password:
        add_user(settings.admin_email, hash_password(settings.admin_password), role="admin")
        print(f"[startup] admin created: {settings.admin_email}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_admin()
    yield


app = FastAPI(title="Notes API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time-ms"] = f"{elapsed_ms:.2f}"
    print(f"{request.method} {request.url.path} -> {response.status_code} ({elapsed_ms:.2f} ms)")
    return response


register_exception_handlers(app)
app.include_router(auth.router)
app.include_router(notes.router)
