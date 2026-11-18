from fastapi import FastAPI

from common import DbSession, User, login_router, seed_demo_users, settings

seed_demo_users()
app = FastAPI(title="Task 6 - me")
app.include_router(login_router)


def get_current_user():
    pass


@app.get("/auth/me")
def read_me():
    return {"todo": "implement me"}
