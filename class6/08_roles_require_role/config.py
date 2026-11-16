"""
Settings
========
pydantic-settings reads values from environment variables AND from the `.env`
file next to this file. Names are case-insensitive: SECRET_KEY -> secret_key.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",  # always the .env in THIS folder
        extra="ignore",  # ignore unknown keys in .env
    )

    # No default value -> REQUIRED. Missing from .env = the app refuses to start.
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite:///./roles.db"


# Created ONCE at import time. Other modules do: `from config import settings`
settings = Settings()
