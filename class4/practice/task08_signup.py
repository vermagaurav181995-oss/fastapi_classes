from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI(title="Task 8 - signup")


class Signup(BaseModel):
    email: str
    password: str
    confirm_password: str


@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(data: Signup):
    return {"email": data.email}
