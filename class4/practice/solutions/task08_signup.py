from typing import Self

from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr, model_validator

app = FastAPI(title="Task 8 - solution")


class Signup(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("passwords do not match")
        return self


@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(data: Signup):
    return {"email": data.email}
