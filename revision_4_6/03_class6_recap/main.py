import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import admin, auth
from security import hash_password
from storage import USERS, add_user


def seed_first_admin() -> None:
    has_admin = any(user["role"] == "admin" for user in USERS.values())
    if has_admin or not (settings.admin_email and settings.admin_password):
        print("[lifespan] no admin created")
        return
    add_user(settings.admin_email, hash_password(settings.admin_password), role="admin")
    print(f"[lifespan] admin created: {settings.admin_email}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[lifespan] startup")
    seed_first_admin()
    yield
    print("[lifespan] shutdown")


app = FastAPI(title="03 - Class 6 Recap", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time-ms"] = f"{elapsed_ms:.2f}"
    print(f"{request.method} {request.url.path} -> {response.status_code} ({elapsed_ms:.2f} ms)")
    return response


app.include_router(auth.router)
app.include_router(admin.router)
