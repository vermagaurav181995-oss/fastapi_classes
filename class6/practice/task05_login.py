"""
Task 5 - POST /auth/login
Use OAuth2PasswordRequestForm (username = email). Return
{"access_token": ..., "token_type": "bearer"}, or 401 "Incorrect email or password".
Then DECODE the token you created and print the payload.
Demo user: student@example.com / password123
Run:  fastapi dev task05_login.py
"""

from fastapi import FastAPI

from common import DbSession, create_access_token, seed_demo_users, settings, verify_password  # noqa: F401

seed_demo_users()
app = FastAPI(title="Task 5 - login")


@app.post("/auth/login")
def login(db: DbSession):
    # TODO: add  form: Annotated[OAuth2PasswordRequestForm, Depends()]
    # TODO: find the user by email (form.username), check the password -> 401 otherwise
    #       (same message for both cases + headers={"WWW-Authenticate": "Bearer"})
    # TODO: token = create_access_token(user.id)
    # TODO: print(jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm]))
    return {"todo": "implement me"}
