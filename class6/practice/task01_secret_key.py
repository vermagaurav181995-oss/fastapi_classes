from pathlib import Path

from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict

HERE = Path(__file__).parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=HERE / ".env", extra="ignore")
    secret_key: str = "dev-secret"
    algorithm: str = "HS256"


settings = Settings()
app = FastAPI(title="Task 1 - SECRET_KEY")


@app.get("/check")
def check():
    return {"todo": "implement me"}
