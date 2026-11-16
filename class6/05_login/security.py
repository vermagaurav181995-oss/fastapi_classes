"""Security helpers: password hashing, JWT tokens."""

from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from config import settings

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
