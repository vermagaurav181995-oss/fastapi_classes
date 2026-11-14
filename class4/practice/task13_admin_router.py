from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException

app = FastAPI(title="Task 13 - admin router")

API_KEY = "letmein"


def verify_api_key():
    pass


admin = APIRouter(prefix="/admin")


@admin.get("/dashboard")
def dashboard():
    return {"message": "Welcome, admin"}


app.include_router(admin)


@app.get("/")
def home():
    return {"message": "Public page"}
