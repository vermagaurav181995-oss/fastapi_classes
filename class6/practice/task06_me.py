"""
Task 6 - GET /auth/me with CurrentUser
Write get_current_user yourself (don't import the one from common):
    OAuth2PasswordBearer -> jwt.decode -> db.get(User, int(sub)) -> check is_active
Test: no token (401), fake token (401), real token from POST /auth/login (200).
Run:  fastapi dev task06_me.py   (demo user: student@example.com / password123)
"""

from fastapi import FastAPI

from common import DbSession, User, login_router, seed_demo_users, settings  # noqa: F401

seed_demo_users()
app = FastAPI(title="Task 6 - me")
app.include_router(login_router)

# TODO: oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user():  # TODO: parameters token (Depends(oauth2_scheme)) and db
    # TODO: decode, load the user, raise 401 "Could not validate credentials" on any problem
    pass


# TODO: CurrentUser = Annotated[User, Depends(get_current_user)]


@app.get("/auth/me")
def read_me():  # TODO: user: CurrentUser
    return {"todo": "implement me"}
