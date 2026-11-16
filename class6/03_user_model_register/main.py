"""
03 - User model + registration
==============================
models.py   -> the User TABLE (id, email unique, hashed_password, role, is_active)
schemas.py  -> UserCreate (what comes IN) and UserOut (what goes OUT, no password!)
security.py -> hash_password() from example 01

Setup:  cp .env.example .env
Run:    fastapi dev main.py         Docs: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException, status
from sqlalchemy import select

from database import Base, DbSession, engine
from models import User
from schemas import UserCreate, UserOut
from security import hash_password

# Create the tables on startup (example 14 shows the nicer "lifespan" way)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="03 - User Model & Register")


@app.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: DbSession):
    # Step 1: Pydantic already checked the email format and password length (422 if bad)
    # Step 2: is the email taken? -> 409 Conflict
    if db.scalar(select(User).where(User.email == data.email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    # Step 3: store the HASH, never the password itself
    user = User(email=data.email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)  # load id, role, is_active defaults from the DB

    # Step 4: return the ORM object; response_model=UserOut drops hashed_password
    return user


@app.get("/users", response_model=list[UserOut])
def list_users(db: DbSession):
    return db.scalars(select(User)).all()


# ---------------------------------------------------------------------------
# TRY IT
# ---------------------------------------------------------------------------
# POST /auth/register {"email": "ada@example.com", "password": "supersecret"}
#   -> 201 {"id": 1, "email": "ada@example.com", "role": "user", "is_active": true}
#      (no password and no hash in the response!)
# GET  /users  -> 200 [ {...ada...} ]
# Open users.db (e.g. VS Code "SQLite Viewer"): hashed_password starts with "$argon2id$"
#
# These should FAIL:
# same register request again                          -> 409 "Email already registered"
# {"email": "ada2@example.com", "password": "short"}  -> 422 "at least 8 characters"
# {"email": "not-an-email", "password": "supersecret"} -> 422 "value is not a valid email"
