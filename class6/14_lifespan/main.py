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
    print("[lifespan] STARTUP: creating tables")
    Base.metadata.create_all(bind=engine)
    create_first_admin()
    yield
    print("[lifespan] SHUTDOWN: closing database connections")
    engine.dispose()


app = FastAPI(title="14 - Lifespan", lifespan=lifespan)
app.include_router(auth.router)


@app.get("/admin/users", response_model=list[UserOut], tags=["admin"])
def list_users(admin: AdminUser, db: DbSession):
    return db.scalars(select(User).order_by(User.id)).all()
