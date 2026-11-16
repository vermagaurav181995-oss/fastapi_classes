"""Security helpers: password hashing."""

from pwdlib import PasswordHash

# ---- 1. Password hashing -------------------------------------------------
# recommended() = Argon2: slow on purpose, and salted (same password -> different hash)
password_hash = PasswordHash.recommended()


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)
