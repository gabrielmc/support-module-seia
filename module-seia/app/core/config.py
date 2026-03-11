from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import List


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
    
    # ===== DATABASE - TREINAMENTO =====
    DATABASE_TREINAMENTO_HOST: str
    DATABASE_TREINAMENTO_PORT: int = 5432
    DATABASE_TREINAMENTO_NAME: str
    DATABASE_TREINAMENTO_USER: str
    DATABASE_TREINAMENTO_PASSWORD: str

    # ===== APP =====
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 9000
    LOG_LEVEL: str = "INFO"
    
    # ===== CORS =====
    CORS_ORIGINS: List[str] = []
    
    # ===== JBOSS =====
    JBOSS_USER: str
    JBOSS_PASS: str
    JBOSS_URL_DSV: str
    JBOSS_URL_HML: str
    
    JBOSS_URL_TREINAMENTO: str
    JBOSS_USER_TREINAMENTO: str
    JBOSS_PASS_TREINAMENTO: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="forbid"
    )

settings = Settings()
