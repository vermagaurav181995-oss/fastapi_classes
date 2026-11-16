"""
Task 11 - CORS
Allow a frontend on http://localhost:5173 to call this API.
Run:  fastapi dev task11_cors.py
Check: a request with header  Origin: http://localhost:5173  gets back
       access-control-allow-origin: http://localhost:5173
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # noqa: F401

from common import CurrentUser, login_router, seed_demo_users

seed_demo_users()
app = FastAPI(title="Task 11 - CORS")

# TODO: app.add_middleware(CORSMiddleware, allow_origins=[...], allow_methods=..., allow_headers=...)

app.include_router(login_router)


@app.get("/auth/me")
def read_me(user: CurrentUser):
    return {"email": user.email}
