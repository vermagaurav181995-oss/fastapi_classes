from fastapi import FastAPI
from pydantic import BaseModel

from common import CurrentUser, DbSession, hash_password, login_router, seed_demo_users, verify_password

seed_demo_users()
app = FastAPI(title="Task 10 - change password")
app.include_router(login_router)


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


@app.patch("/auth/me/password")
def change_password(data: PasswordChange):
    return {"todo": "implement me"}
