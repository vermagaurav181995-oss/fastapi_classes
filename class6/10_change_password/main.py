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
    if not verify_password(data.old_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")

    if data.old_password == data.new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be different")

    user.hashed_password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password changed. Log in again with the new password."}
