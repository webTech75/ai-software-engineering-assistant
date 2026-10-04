from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    upload_folder: str
    openai_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

# Read .env once and cache the settings for future use
@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()