"""
Task 1 - SECRET_KEY must be required
1. cp .env.example .env  and put a real secret in it:
       python -c "import secrets; print(secrets.token_hex(32))"
2. Make the app REFUSE to start when SECRET_KEY is missing.
Run:  fastapi dev task01_secret_key.py
Check: with the key -> GET /check is 200. Delete the line -> startup fails with
       "ValidationError ... secret_key  Field required".
"""

from pathlib import Path

from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict

HERE = Path(__file__).parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=HERE / ".env", extra="ignore")
    secret_key: str = "dev-secret"  # TODO: remove the default so the field is REQUIRED
    algorithm: str = "HS256"


settings = Settings()
app = FastAPI(title="Task 1 - SECRET_KEY")


@app.get("/check")
def check():
    # TODO: return whether the key is loaded and its length (never the key itself!)
    return {"todo": "implement me"}
