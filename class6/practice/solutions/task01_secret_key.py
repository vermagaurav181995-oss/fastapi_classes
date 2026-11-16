"""Solution 1: SECRET_KEY is required -> the app refuses to start without it."""

from pathlib import Path

from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict

HERE = Path(__file__).parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(HERE.parent / ".env", HERE / ".env"), extra="ignore")
    secret_key: str  # no default -> required
    algorithm: str = "HS256"


settings = Settings()  # raises ValidationError "secret_key Field required" if missing
app = FastAPI(title="Task 1 - solution")


@app.get("/check")
def check():
    return {"secret_key_loaded": True, "length": len(settings.secret_key)}

# With SECRET_KEY in .env: GET /check -> 200
# Without it: `fastapi dev` stops with "ValidationError ... secret_key Field required"
