import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from exceptions import register_exception_handlers
from routers import auth, items
from security import hash_password
from storage import add_user, find_user_by_email


def seed_admin() -> None:
    if settings.admin_email and settings.admin_password and not find_user_by_email(settings.admin_email):
        add_user(settings.admin_email, hash_password(settings.admin_password), role="admin")
        print(f"[startup] admin created: {settings.admin_email}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_admin()
    yield


app = FastAPI(
    title="My Capstone API",
    lifespan=lifespan,
    docs_url=None if settings.is_production else "/docs",
    redoc_url=None if settings.is_production else "/redoc",
    openapi_url=None if settings.is_production else "/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
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


register_exception_handlers(app)
app.include_router(auth.router)
app.include_router(items.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
