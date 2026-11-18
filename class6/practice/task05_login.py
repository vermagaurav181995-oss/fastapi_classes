from fastapi import FastAPI

from common import DbSession, create_access_token, seed_demo_users, settings, verify_password

seed_demo_users()
app = FastAPI(title="Task 5 - login")


@app.post("/auth/login")
def login(db: DbSession):
    return {"todo": "implement me"}
