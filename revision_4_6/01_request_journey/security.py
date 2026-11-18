from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from config import settings
from storage import USERS

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


def create_access_token(user_id: int, expires_minutes: int | None = None) -> str:
    minutes = settings.access_token_expire_minutes if expires_minutes is None else expires_minutes
    payload = {"sub": str(user_id), "exp": datetime.now(timezone.utc) + timedelta(minutes=minutes)}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id = int(jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise invalid_credentials
    user = USERS.get(user_id)
    if user is None:
        raise invalid_credentials
    return user


CurrentUser = Annotated[dict, Depends(get_current_user)]


def require_role(*roles: str):
    def role_checker(user: CurrentUser) -> dict:
        if user["role"] not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return user

    return role_checker


AdminUser = Annotated[dict, Depends(require_role("admin"))]
