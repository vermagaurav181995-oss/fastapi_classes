"""
Task 7 - Token expiry
1. In practice/.env set  ACCESS_TOKEN_EXPIRE_MINUTES=1
2. Log in, call GET /auth/me -> 200. Wait 60+ seconds, call it again -> 401.
3. Add GET /auth/token-info that shows the token's "exp" value.
Run:  fastapi dev task07_token_expiry.py
"""

from fastapi import FastAPI

from common import CurrentUser, login_router, oauth2_scheme, seed_demo_users, settings  # noqa: F401

seed_demo_users()
app = FastAPI(title="Task 7 - expiry")
app.include_router(login_router)


@app.get("/auth/me")
def read_me(user: CurrentUser):
    return {"email": user.email}


@app.get("/auth/token-info")
def token_info(user: CurrentUser):
    # TODO: also receive the raw token: token: Annotated[str, Depends(oauth2_scheme)]
    # TODO: decode it and return {"expire_minutes_setting": ..., "exp": ...}
    return {"todo": "implement me"}
