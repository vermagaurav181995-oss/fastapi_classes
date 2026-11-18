from fastapi import FastAPI

from database import Base, engine
from routers import auth, books, public

Base.metadata.create_all(bind=engine)

app = FastAPI(title="07 - Protect a Router")
app.include_router(auth.router)
app.include_router(public.router)
app.include_router(books.router)
