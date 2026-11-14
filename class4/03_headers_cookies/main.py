from typing import Annotated

from fastapi import Cookie, FastAPI, Header, HTTPException, Response

app = FastAPI(title="03 - Headers & Cookies")

VALID_TOKEN = "secret-token"


@app.get("/headers")
def read_headers(
    user_agent: Annotated[str | None, Header()] = None,
    x_token: Annotated[str | None, Header()] = None,
):
    return {"user_agent": user_agent, "x_token": x_token}


@app.get("/secure")
def secure(x_token: Annotated[str, Header()]):
    if x_token != VALID_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid X-Token")
    return {"message": "Token accepted"}


@app.get("/set-cookie")
def set_cookie(response: Response):
    response.set_cookie(key="session_id", value="abc123", httponly=True)
    return {"message": "Cookie 'session_id' set. Now call GET /read-cookie"}


@app.get("/read-cookie")
def read_cookie(session_id: Annotated[str | None, Cookie()] = None):
    if session_id is None:
        raise HTTPException(status_code=401, detail="No session_id cookie. Call /set-cookie first.")
    return {"session_id": session_id}


@app.get("/clear-cookie")
def clear_cookie(response: Response):
    response.delete_cookie("session_id")
    return {"message": "Cookie removed"}
