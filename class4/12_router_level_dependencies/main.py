from fastapi import FastAPI

from routers import admin, public

app = FastAPI(title="12 - Router-level Dependencies")

app.include_router(public.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "See /public/* (open) and /admin/* (needs X-API-Key)"}
