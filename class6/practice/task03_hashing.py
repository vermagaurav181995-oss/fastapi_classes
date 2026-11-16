"""
Task 3 - Password hashing
Write hash_password / verify_password with pwdlib, then hash "secret123" TWICE
and print both hashes. Are they equal? Do both verify?
Run:  fastapi dev task03_hashing.py   (look at the terminal)
"""

from fastapi import FastAPI
from pwdlib import PasswordHash  # noqa: F401

# TODO: password_hash = PasswordHash.recommended()


def hash_password(plain: str) -> str:
    # TODO
    return plain


def verify_password(plain: str, hashed: str) -> bool:
    # TODO
    return False


# TODO: hash "secret123" twice and print both hashes + whether they are equal

app = FastAPI(title="Task 3 - hashing")


@app.get("/hash-twice")
def hash_twice(password: str = "secret123"):
    # TODO: return {"hash_1": ..., "hash_2": ..., "equal": ...}
    return {"todo": "implement me"}
