"""Security helpers: JWT tokens."""

from datetime import datetime, timedelta, timezone

import jwt

from config import settings


# ---- JWT access tokens ------------------------------------------------
def create_access_token(user_id: int, expires_minutes: int | None = None) -> str:
    if expires_minutes is None:
        expires_minutes = settings.access_token_expire_minutes
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {"sub": str(user_id), "exp": expire}  # "sub" must be a STRING
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict:
    # Checks the signature AND "exp". Raises jwt.InvalidTokenError when bad.
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
