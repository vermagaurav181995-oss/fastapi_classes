from fastapi import FastAPI
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


first, second = hash_password("secret123"), hash_password("secret123")
print("hash 1:", first)
print("hash 2:", second)
print("equal?", first == second, "| both verify?", verify_password("secret123", first) and verify_password("secret123", second))

app = FastAPI(title="Task 3 - solution")


@app.get("/hash-twice")
def hash_twice(password: str = "secret123"):
    a, b = hash_password(password), hash_password(password)
    return {"hash_1": a, "hash_2": b, "equal": a == b}


@app.get("/verify")
def verify(password: str, attempt: str):
    return {"is_valid": verify_password(attempt, hash_password(password))}
