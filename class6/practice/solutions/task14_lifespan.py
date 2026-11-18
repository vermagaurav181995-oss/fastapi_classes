from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select

from common import Base, SessionLocal, User, engine, hash_password, login_router, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup")
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        has_admin = db.scalar(select(User).where(User.role == "admin")) is not None
        if not has_admin and settings.admin_email and settings.admin_password:
            db.add(User(email=settings.admin_email, hashed_password=hash_password(settings.admin_password), role="admin"))
            db.commit()
            print(f"created admin {settings.admin_email}")
    yield
    print("shutdown")


app = FastAPI(title="Task 14 - solution", lifespan=lifespan)
app.include_router(login_router)
