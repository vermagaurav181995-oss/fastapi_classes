from typing import Annotated

from fastapi import FastAPI, Query
from pwdlib import PasswordHash

app = FastAPI(title="01 - Password Hashing")

password_hash = PasswordHash.recommended()


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


PasswordQuery = Annotated[str, Query(min_length=1, max_length=128)]


@app.get("/demo/hash")
def demo_hash(password: PasswordQuery = "secret123"):
    first = hash_password(password)
    second = hash_password(password)
    return {
        "password": password,
        "hash_1": first,
        "hash_2": second,
        "hashes_are_equal": first == second,
        "both_verify": verify_password(password, first) and verify_password(password, second),
    }


@app.get("/demo/verify")
def demo_verify(password: PasswordQuery = "secret123", attempt: PasswordQuery = "secret123"):
    stored = hash_password(password)
    return {"stored_hash": stored, "attempt": attempt, "is_valid": verify_password(attempt, stored)}
