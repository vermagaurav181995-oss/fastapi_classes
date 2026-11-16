"""
02 - Settings and the SECRET_KEY
================================
Secrets must NOT live in your code (or on GitHub). They live in a `.env` file
that is listed in .gitignore. config.py loads it with pydantic-settings.

SECRET_KEY has NO default -> if it's missing, the app refuses to start:
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings
    secret_key
      Field required [type=missing, ...]

Setup:  cp .env.example .env    (then put a real secret in it)
Run:    fastapi dev main.py
"""

from fastapi import FastAPI, HTTPException

from config import settings  # <- this line crashes if SECRET_KEY is missing

app = FastAPI(title="02 - Settings & SECRET_KEY")


@app.get("/settings")
def show_settings():
    # Show the NON-secret settings. Never return the secret itself!
    return {
        "algorithm": settings.algorithm,
        "access_token_expire_minutes": settings.access_token_expire_minutes,
        "database_url": settings.database_url,
        "secret_key_length": len(settings.secret_key),
        "secret_key_preview": settings.secret_key[:4] + "...",
    }


@app.get("/settings/{name}")
def show_one_setting(name: str):
    # Only these names may be read. Anything else (like secret_key) -> 404
    public = {"algorithm", "access_token_expire_minutes", "database_url"}
    if name not in public:
        raise HTTPException(status_code=404, detail=f"No public setting called '{name}'")
    return {name: getattr(settings, name)}


# ---------------------------------------------------------------------------
# TRY IT
# ---------------------------------------------------------------------------
# GET /settings
#   -> 200 {"algorithm": "HS256", "access_token_expire_minutes": 30,
#           "database_url": "sqlite:///./settings_demo.db", "secret_key_length": 64, ...}
# GET /settings/algorithm         -> 200 {"algorithm": "HS256"}
# Change ACCESS_TOKEN_EXPIRE_MINUTES=5 in .env -> the dev server reloads -> /settings shows 5
#
# These should FAIL:
# GET /settings/secret_key        -> 404 "No public setting called 'secret_key'"
# Delete the SECRET_KEY line from .env and restart -> the app does not start:
#   "ValidationError ... secret_key  Field required"
