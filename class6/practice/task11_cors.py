from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common import CurrentUser, login_router, seed_demo_users

seed_demo_users()
app = FastAPI(title="Task 11 - CORS")


app.include_router(login_router)


@app.get("/auth/me")
def read_me(user: CurrentUser):
    return {"email": user.email}
