import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from exceptions import register_exception_handlers
from routers import auth, books
from security import hash_password
from storage import USERS

DEMO_USERS = [
    ("admin@example.com", "admin12345", "admin"),
    ("user@example.com", "user12345", "user"),
]


def seed_users() -> None:
    for user_id, (email, password, role) in enumerate(DEMO_USERS, start=1):
        USERS[user_id] = {"id": user_id, "email": email, "hashed_password": hash_password(password), "role": role}


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_users()
    print(f"[startup] seeded {len(USERS)} users")
    yield
    print("[shutdown] bye")


app = FastAPI(title="01 - Request Journey", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_and_time_requests(request: Request, call_next):
    print(f"[middleware] -> {request.method} {request.url.path}")
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time-ms"] = f"{elapsed_ms:.2f}"
    print(f"[middleware] <- {request.method} {request.url.path} {response.status_code} ({elapsed_ms:.2f} ms)")
    return response


register_exception_handlers(app)
app.include_router(auth.router)
app.include_router(books.router)
