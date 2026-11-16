"""
Task 14 - lifespan creates the first admin
On startup: create the tables, then create an admin from ADMIN_EMAIL /
ADMIN_PASSWORD in practice/.env, but only if NO admin exists yet.
Print something on startup and on shutdown.
Run:  fastapi dev task14_lifespan.py   then log in as that admin via POST /auth/login
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from common import Base, SessionLocal, User, engine, hash_password, login_router, settings  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: print("startup") and Base.metadata.create_all(bind=engine)
    # TODO: with SessionLocal() as db: if no User with role "admin" exists and
    #       settings.admin_email / settings.admin_password are set -> add one, commit
    yield
    # TODO: print("shutdown")


app = FastAPI(title="Task 14 - lifespan", lifespan=lifespan)
app.include_router(login_router)
