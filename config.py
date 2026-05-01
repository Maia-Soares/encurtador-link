from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Configuração moderna do Pydantic v2
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8")

    # Banco de Dados
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Cache
    CACHE_TTL_SECONDS: int = 3600


# Cria uma instância única para usar em todo o projeto
settings = Settings()
