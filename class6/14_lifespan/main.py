"""
14 - Lifespan: startup and shutdown code
========================================
Examples 03-13 ran `create_all()` and seeding at IMPORT time. The proper place
is a LIFESPAN function:
    code before `yield` -> runs once when the server STARTS
    code after  `yield` -> runs once when the server STOPS (Ctrl+C)
Here startup creates the tables and the first admin from ADMIN_EMAIL /
ADMIN_PASSWORD in .env, but ONLY if no admin exists yet.

Setup:  cp .env.example .env
Run:    fastapi dev main.py   and watch the terminal (start AND Ctrl+C)
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select

from config import settings
from database import Base, DbSession, SessionLocal, engine
from models import User
from routers import auth
from schemas import UserOut
from security import AdminUser, hash_password


def create_first_admin() -> None:
    if not (settings.admin_email and settings.admin_password):
        print("[lifespan] ADMIN_EMAIL / ADMIN_PASSWORD not set: no admin created")
        return
    with SessionLocal() as db:
        if db.scalar(select(User).where(User.role == "admin")) is not None:
            print("[lifespan] an admin already exists: nothing to do")
            return
        db.add(User(email=settings.admin_email, hashed_password=hash_password(settings.admin_password), role="admin"))
        db.commit()
        print(f"[lifespan] created first admin: {settings.admin_email}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- STARTUP ----
    print("[lifespan] STARTUP: creating tables")
    Base.metadata.create_all(bind=engine)
    create_first_admin()
    yield  # <- the app serves requests while we're paused here
    # ---- SHUTDOWN ----
    print("[lifespan] SHUTDOWN: closing database connections")
    engine.dispose()


app = FastAPI(title="14 - Lifespan", lifespan=lifespan)
app.include_router(auth.router)


@app.get("/admin/users", response_model=list[UserOut], tags=["admin"])
def list_users(admin: AdminUser, db: DbSession):
    return db.scalars(select(User).order_by(User.id)).all()


# ---------------------------------------------------------------------------
# TRY IT
# ---------------------------------------------------------------------------
# Start the server -> terminal: "[lifespan] STARTUP ..." + "created first admin: admin@example.com"
# Restart it       -> terminal: "an admin already exists: nothing to do"
# POST /auth/login FORM username=admin@example.com&password=admin12345 -> 200 {adminToken}
# GET  /auth/me      + adminToken -> 200 {"email": "admin@example.com", "role": "admin", ...}
# GET  /admin/users  + adminToken -> 200 [ ...all users... ]
# Ctrl+C           -> terminal: "[lifespan] SHUTDOWN: closing database connections"
#
# These should FAIL:
# POST /auth/register {"email": "ana@example.com", "password": "anapass123"} -> 201, then
# GET  /admin/users  + ana's token -> 403 "Not enough permissions"
# GET  /admin/users  (no token)    -> 401
# POST /auth/register with admin@example.com -> 409 "Email already registered"
