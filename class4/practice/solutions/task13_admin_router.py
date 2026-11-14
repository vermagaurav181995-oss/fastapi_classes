from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException

app = FastAPI(title="Task 13 - solution")

API_KEY = "letmein"


def verify_api_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")


admin = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(verify_api_key)])


@admin.get("/dashboard")
def dashboard():
    return {"message": "Welcome, admin"}


app.include_router(admin)


@app.get("/")
def home():
    return {"message": "Public page"}
