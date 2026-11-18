from contextlib import asynccontextmanager

from fastapi import FastAPI

from common import Base, SessionLocal, User, engine, hash_password, login_router, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Task 14 - lifespan", lifespan=lifespan)
app.include_router(login_router)
