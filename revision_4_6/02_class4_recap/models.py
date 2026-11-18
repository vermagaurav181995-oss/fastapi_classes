from typing import Annotated, Self

from pydantic import BaseModel, EmailStr, Field, model_validator


class ItemCreate(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=50)]
    price: Annotated[float, Field(gt=0)]
    in_stock: bool = True


class ItemUpdate(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=50)] | None = None
    price: Annotated[float, Field(gt=0)] | None = None
    in_stock: bool | None = None


class Registration(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]
    confirm_password: str

    @model_validator(mode="after")
    def passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("passwords do not match")
        return self
