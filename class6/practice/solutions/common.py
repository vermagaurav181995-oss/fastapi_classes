from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

HERE = Path(__file__).parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(HERE.parent / ".env", HERE / ".env"), extra="ignore")
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite:///./practice.db"
    admin_email: str | None = None
    admin_password: str | None = None


settings = Settings()

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str]
    role: Mapped[str] = mapped_column(String(20), default="user")
    is_active: Mapped[bool] = mapped_column(default=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]

password_hash = PasswordHash.recommended()


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


def create_access_token(user_id: int, expires_minutes: int | None = None) -> str:
    minutes = settings.access_token_expire_minutes if expires_minutes is None else expires_minutes
    payload = {"sub": str(user_id), "exp": datetime.now(timezone.utc) + timedelta(minutes=minutes)}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DbSession) -> User:
    error = HTTPException(status.HTTP_401_UNAUTHORIZED, "Could not validate credentials", {"WWW-Authenticate": "Bearer"})
    try:
        user = db.get(User, int(jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])["sub"]))
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise error
    if user is None or not user.is_active:
        raise error
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def seed_demo_users() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        for email, password, role in [("student@example.com", "password123", "user"), ("admin@example.com", "admin12345", "admin")]:
            if db.scalar(select(User).where(User.email == email)) is None:
                db.add(User(email=email, hashed_password=hash_password(password), role=role))
        db.commit()


login_router = APIRouter(prefix="/auth", tags=["auth"])


@login_router.post("/login")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    user = db.scalar(select(User).where(User.email == form.username))
    if user is None or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect email or password", {"WWW-Authenticate": "Bearer"})
    return {"access_token": create_access_token(user.id), "token_type": "bearer"}
