"""
10 - Changing your password
===========================
PATCH /auth/me/password needs:
  * a valid token          -> WHO is changing it        (401 otherwise)
  * the OLD password       -> proves it's really them   (400 if wrong)
    (protects against someone using a laptop you left logged in)
  * a NEW password         -> min 8 chars               (422 otherwise)

Setup:  cp .env.example .env
Run:    fastapi dev main.py         Docs: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException, status

from database import Base, DbSession, engine
from routers import auth
from schemas import PasswordChange
from security import CurrentUser, hash_password, verify_password

Base.metadata.create_all(bind=engine)

app = FastAPI(title="10 - Change Password")
app.include_router(auth.router)


@app.patch("/auth/me/password", tags=["auth"])
def change_password(data: PasswordChange, user: CurrentUser, db: DbSession):
    # Step 1: check the OLD password against the stored hash
    if not verify_password(data.old_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")

    # Step 2: refuse "changing" to the same password
    if data.old_password == data.new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be different")

    # Step 3: store the HASH of the new password.
    # `user` came from get_current_user's session, the same `db` used here,
    # because FastAPI caches get_db within one request.
    user.hashed_password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password changed. Log in again with the new password."}


# ---------------------------------------------------------------------------
# TRY IT
# ---------------------------------------------------------------------------
# POST  /auth/register {"email": "ada@example.com", "password": "supersecret"} -> 201
# POST  /auth/login FORM username=ada@example.com&password=supersecret       -> 200 {token}
# PATCH /auth/me/password {"old_password": "supersecret", "new_password": "evenmoresecret"}
#       + token -> 200 {"message": "Password changed. ..."}
# POST  /auth/login with password=evenmoresecret -> 200
#
# These should FAIL:
# POST  /auth/login with the OLD password=supersecret                      -> 401
# PATCH /auth/me/password {"old_password": "WRONG", ...} + token           -> 400 "Old password is incorrect"
# PATCH /auth/me/password {"old_password": "...", "new_password": "short"} -> 422
# PATCH /auth/me/password (no token)                                       -> 401
# Note: tokens issued BEFORE the change still work until they expire (JWTs are stateless).
