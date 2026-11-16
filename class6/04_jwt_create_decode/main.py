"""
04 - Creating and decoding JWTs
===============================
A JWT has 3 parts:  HEADER.PAYLOAD.SIGNATURE   (each base64url-encoded)
* The payload is NOT encrypted: anyone can read it (paste one into jwt.io).
* The SIGNATURE is made with SECRET_KEY: nobody can CHANGE the payload without
  the secret, and "exp" makes the token stop working after a while.
Our payload:  {"sub": "<user id as a string>", "exp": <unix timestamp>}

Setup:  cp .env.example .env
Run:    fastapi dev main.py         Docs: http://127.0.0.1:8000/docs
"""

import base64
import json
from typing import Annotated

import jwt
from fastapi import FastAPI, HTTPException, Query

from security import create_access_token, decode_access_token

app = FastAPI(title="04 - JWT create & decode")


def try_decode(token: str) -> dict:
    """Decode a token, turning PyJWT errors into a 401 with a readable reason."""
    try:
        return decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as exc:  # parent of all other JWT errors
        raise HTTPException(status_code=401, detail=f"Invalid token: {exc}")


@app.get("/demo/token")
def make_token(user_id: Annotated[int, Query(ge=1)] = 1):
    token = create_access_token(user_id)
    # Peek at the payload WITHOUT checking the signature (only for teaching!)
    peek = jwt.decode(token, options={"verify_signature": False})
    return {"access_token": token, "payload": peek}


@app.get("/demo/decode")
def decode_token(token: str):
    return {"valid": True, "payload": try_decode(token)}


@app.get("/demo/tampered")
def tampered_token():
    token = create_access_token(user_id=1)
    header, payload, signature = token.split(".")
    # An attacker changes "sub" to "999" but can't re-sign without the SECRET_KEY
    data = json.loads(base64.urlsafe_b64decode(payload + "=="))
    data["sub"] = "999"
    fake_payload = base64.urlsafe_b64encode(json.dumps(data).encode()).rstrip(b"=").decode()
    fake_token = f"{header}.{fake_payload}.{signature}"
    return {"tampered_token": fake_token, "decode_result": try_decode(fake_token)}  # -> 401


@app.get("/demo/expired")
def expired_token():
    token = create_access_token(user_id=1, expires_minutes=-1)  # expired 1 minute ago
    return {"expired_token": token, "decode_result": try_decode(token)}  # -> 401


# ---------------------------------------------------------------------------
# TRY IT
# ---------------------------------------------------------------------------
# GET /demo/token?user_id=7  -> 200 {"access_token": "eyJ...", "payload": {"sub": "7", "exp": 17...}}
# GET /demo/decode?token=<paste the token>  -> 200 {"valid": true, "payload": {"sub": "7", ...}}
#
# These should FAIL:
# GET /demo/tampered         -> 401 "Invalid token: Signature verification failed"
# GET /demo/expired          -> 401 "Token has expired"
# GET /demo/decode?token=abc -> 401 "Invalid token: Not enough segments"
# GET /demo/token?user_id=0  -> 422 (user_id must be >= 1)
# Change SECRET_KEY in .env (server reloads) -> old tokens now fail with 401
