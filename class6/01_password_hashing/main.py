"""
01 - Password hashing with pwdlib (Argon2)
==========================================
NEVER store a plain password. Store a HASH: a one-way scramble of it.
* hash_password("secret")    -> "$argon2id$v=19$m=65536,t=3,p=4$<salt>$<hash>"
* verify_password("secret", stored_hash) -> True / False
Each hash includes a random SALT, so hashing the same password twice gives two
DIFFERENT strings, and both still verify. That defeats "rainbow table" attacks.

Run (from inside this folder):  fastapi dev main.py
Docs:                           http://127.0.0.1:8000/docs
"""

from typing import Annotated

from fastapi import FastAPI, Query
from pwdlib import PasswordHash

app = FastAPI(title="01 - Password Hashing")

# Step 1: create the hasher once. recommended() = Argon2id with safe settings.
password_hash = PasswordHash.recommended()


# Step 2: two small helpers that the rest of the course reuses
def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


PasswordQuery = Annotated[str, Query(min_length=1, max_length=128)]


@app.get("/demo/hash")
def demo_hash(password: PasswordQuery = "secret123"):
    # Step 3: hash the SAME password twice
    first = hash_password(password)
    second = hash_password(password)
    return {
        "password": password,
        "hash_1": first,
        "hash_2": second,
        "hashes_are_equal": first == second,  # False -> random salt!
        "both_verify": verify_password(password, first) and verify_password(password, second),
    }


@app.get("/demo/verify")
def demo_verify(password: PasswordQuery = "secret123", attempt: PasswordQuery = "secret123"):
    # Step 4: hash `password` (like at register), then check `attempt` (like at login)
    stored = hash_password(password)
    return {"stored_hash": stored, "attempt": attempt, "is_valid": verify_password(attempt, stored)}


# ---------------------------------------------------------------------------
# TRY IT
# ---------------------------------------------------------------------------
# GET /demo/hash?password=secret123
#   -> 200 {"hash_1": "$argon2id$...", "hash_2": "$argon2id$...",
#           "hashes_are_equal": false, "both_verify": true}
# GET /demo/verify?password=secret123&attempt=secret123  -> 200 {"is_valid": true, ...}
# GET /demo/verify?password=secret123&attempt=wrong      -> 200 {"is_valid": false, ...}
#
# These should FAIL:
# GET /demo/hash?password=           -> 422 "String should have at least 1 character"
# GET /demo/verify?attempt=<129+ chars> -> 422 "String should have at most 128 characters"
