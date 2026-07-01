import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


def _default_env_file() -> Optional[str]:
    backend_env = Path(__file__).resolve().parents[2] / ".env"
    if backend_env.exists():
        return str(backend_env)
    return None


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://dmed:dmed123@127.0.0.1:5432/dmed"
    REDIS_URL: str = "redis://127.0.0.1:6379/0"
    SECRET_KEY: str = "dmed-local-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USER: str = "noreply@dmed.local"
    EMAIL_PASS: str = ""
    EMR_API_URL: Optional[str] = None
    ENVIRONMENT: str = "development"
    FRONTEND_DIR: Optional[str] = None

    class Config:
        env_file = _default_env_file()
        extra = "ignore"


settings = Settings()

if os.environ.get("DMED_FRONTEND_DIR"):
    settings.FRONTEND_DIR = os.environ["DMED_FRONTEND_DIR"]
