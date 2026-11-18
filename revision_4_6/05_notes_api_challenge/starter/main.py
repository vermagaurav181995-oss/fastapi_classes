from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from routers import auth, notes


def seed_admin() -> None:
    raise NotImplementedError


async def log_requests(request: Request, call_next):
    raise NotImplementedError


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Notes API (starter)", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(notes.router)
