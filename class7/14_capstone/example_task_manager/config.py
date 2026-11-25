from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent / ".env", extra="ignore")

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    environment: str = "development"
    allowed_origins: list[str] = ["http://localhost:5173"]
    admin_email: str | None = None
    admin_password: str | None = None

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


settings = Settings()
