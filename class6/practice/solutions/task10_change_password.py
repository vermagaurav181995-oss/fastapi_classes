"""Solution 10: PATCH /auth/me/password that needs the old password."""

from typing import Annotated

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from common import CurrentUser, DbSession, hash_password, login_router, seed_demo_users, verify_password

seed_demo_users()
app = FastAPI(title="Task 10 - solution")
app.include_router(login_router)


class PasswordChange(BaseModel):
    old_password: str
    new_password: Annotated[str, Field(min_length=8)]


@app.patch("/auth/me/password")
def change_password(data: PasswordChange, user: CurrentUser, db: DbSession):
    if not verify_password(data.old_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")
    user.hashed_password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password changed"}

# wrong old password -> 400     correct -> 200, then log in with the new one
