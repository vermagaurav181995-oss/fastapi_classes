"""
Task 10 - PATCH /auth/me/password
Body: {"old_password": ..., "new_password": ...}  (new one at least 8 chars)
* needs a valid token
* 400 if old_password is wrong
Run:  fastapi dev task10_change_password.py
"""

from fastapi import FastAPI
from pydantic import BaseModel

from common import CurrentUser, DbSession, hash_password, login_router, seed_demo_users, verify_password  # noqa: F401

seed_demo_users()
app = FastAPI(title="Task 10 - change password")
app.include_router(login_router)


class PasswordChange(BaseModel):
    old_password: str
    new_password: str  # TODO: min_length=8


@app.patch("/auth/me/password")
def change_password(data: PasswordChange):  # TODO: user: CurrentUser, db: DbSession
    # TODO: verify the old password -> 400 "Old password is incorrect"
    # TODO: store hash_password(new_password) and commit
    return {"todo": "implement me"}
