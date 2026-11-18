from fastapi import FastAPI, HTTPException, status
from sqlalchemy import select

from database import Base, DbSession, engine
from models import User
from schemas import UserCreate, UserOut
from security import hash_password

Base.metadata.create_all(bind=engine)

app = FastAPI(title="03 - User Model & Register")


@app.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: DbSession):
    if db.scalar(select(User).where(User.email == data.email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(email=data.email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.get("/users", response_model=list[UserOut])
def list_users(db: DbSession):
    return db.scalars(select(User)).all()
