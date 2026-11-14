from typing import Self

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator, model_validator

app = FastAPI(title="06 - Validators")


class Register(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("password")
    @classmethod
    def password_long_enough(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("password must be at least 8 characters")
        return value

    @model_validator(mode="after")
    def passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("passwords do not match")
        return self


USERS: dict[str, str] = {}


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: Register):
    if data.email in USERS:
        raise HTTPException(status_code=400, detail="Email already registered")
    USERS[data.email] = data.password
    return {"message": "User registered", "email": data.email}
