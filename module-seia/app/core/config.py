from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    # ===== DATABASE - DSV =====
    DATABASE_DSV_HOST: str
    DATABASE_DSV_PORT: int = 5432
    DATABASE_DSV_NAME: str
    DATABASE_DSV_USER: str
    DATABASE_DSV_PASSWORD: str

    # ===== DATABASE - HML =====
    DATABASE_HML_HOST: str
    DATABASE_HML_PORT: int = 5432
    DATABASE_HML_NAME: str
    DATABASE_HML_USER: str
    DATABASE_HML_PASSWORD: str

    # ===== APP =====
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 9000

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="forbid"
    )


settings = Settings()
