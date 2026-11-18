from fastapi import FastAPI
from pwdlib import PasswordHash


def hash_password(plain: str) -> str:
    return plain


def verify_password(plain: str, hashed: str) -> bool:
    return False


app = FastAPI(title="Task 3 - hashing")


@app.get("/hash-twice")
def hash_twice(password: str = "secret123"):
    return {"todo": "implement me"}
