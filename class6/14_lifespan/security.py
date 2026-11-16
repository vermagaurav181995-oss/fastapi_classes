"""Security helpers: password hashing, JWT tokens, current user, roles."""

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from config import settings
from database import DbSession
from models import User

# ---- 1. Password hashing -------------------------------------------------
# recommended() = Argon2: slow on purpose, and salted (same password -> different hash)
password_hash = PasswordHash.recommended()


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


# ---- 2. JWT access tokens ------------------------------------------------
def create_access_token(user_id: int, expires_minutes: int | None = None) -> str:
    if expires_minutes is None:
        expires_minutes = settings.access_token_expire_minutes
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {"sub": str(user_id), "exp": expire}  # "sub" must be a STRING
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict:
    # Checks the signature AND "exp". Raises jwt.InvalidTokenError when bad.
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])


# ---- 3. The current user -------------------------------------------------
# Reads "Authorization: Bearer <token>". tokenUrl = where /docs' Authorize button logs in.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DbSession) -> User:
    try:
        payload = decode_access_token(token)  # bad signature / expired -> error
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise credentials_exception
    user = db.get(User, user_id)  # the user may have been deleted since
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


# ---- 4. Roles ------------------------------------------------------------
def require_role(*roles: str):
    """Dependency FACTORY: require_role("admin") RETURNS a new dependency."""

    def checker(user: CurrentUser) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return user

    return checker


AdminUser = Annotated[User, Depends(require_role("admin"))]
