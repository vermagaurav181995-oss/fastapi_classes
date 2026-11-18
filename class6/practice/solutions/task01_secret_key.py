from pathlib import Path

from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict

HERE = Path(__file__).parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(HERE.parent / ".env", HERE / ".env"), extra="ignore")
    secret_key: str
    algorithm: str = "HS256"


settings = Settings()
app = FastAPI(title="Task 1 - solution")


@app.get("/check")
def check():
    return {"secret_key_loaded": True, "length": len(settings.secret_key)}
