from fastapi import FastAPI

from common import CurrentUser, login_router, oauth2_scheme, seed_demo_users, settings

seed_demo_users()
app = FastAPI(title="Task 7 - expiry")
app.include_router(login_router)


@app.get("/auth/me")
def read_me(user: CurrentUser):
    return {"email": user.email}


@app.get("/auth/token-info")
def token_info(user: CurrentUser):
    return {"todo": "implement me"}
