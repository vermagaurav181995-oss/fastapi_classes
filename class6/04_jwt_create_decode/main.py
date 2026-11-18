import base64
import json
from typing import Annotated

import jwt
from fastapi import FastAPI, HTTPException, Query

from security import create_access_token, decode_access_token

app = FastAPI(title="04 - JWT create & decode")


def try_decode(token: str) -> dict:
    try:
        return decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail=f"Invalid token: {exc}")


@app.get("/demo/token")
def make_token(user_id: Annotated[int, Query(ge=1)] = 1):
    token = create_access_token(user_id)
    peek = jwt.decode(token, options={"verify_signature": False})
    return {"access_token": token, "payload": peek}


@app.get("/demo/decode")
def decode_token(token: str):
    return {"valid": True, "payload": try_decode(token)}


@app.get("/demo/tampered")
def tampered_token():
    token = create_access_token(user_id=1)
    header, payload, signature = token.split(".")
    data = json.loads(base64.urlsafe_b64decode(payload + "=="))
    data["sub"] = "999"
    fake_payload = base64.urlsafe_b64encode(json.dumps(data).encode()).rstrip(b"=").decode()
    fake_token = f"{header}.{fake_payload}.{signature}"
    return {"tampered_token": fake_token, "decode_result": try_decode(fake_token)}


@app.get("/demo/expired")
def expired_token():
    token = create_access_token(user_id=1, expires_minutes=-1)
    return {"expired_token": token, "decode_result": try_decode(token)}
