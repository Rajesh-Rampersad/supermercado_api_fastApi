from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///supermercado.db"
    SECRET_API_KEY: str = "supersecreto123"

    # Extrae variables del archivo .env si existe
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()