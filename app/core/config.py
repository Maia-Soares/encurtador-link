from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )

    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    CACHE_TTL_SECONDS: int = 3600


settings = Settings()
