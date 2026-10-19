
"""
===============================================================================
File: config.py
Path: app/core/config.py

Description:
    Loads and validates application configuration.

Responsibilities:
    - Read environment variables.
    - Provide strongly typed application settings.
    - Centralize runtime configuration.

Author:
    Amr Elhabbal
===============================================================================
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    database_url: str
    secret_key: str
    algorithm: str
    registration_code: str
    access_token_expire_minutes: int
    upload_folder: str
    frontend_url: str

    openai_api_key: str = ""

    LLM_PROVIDER: str
    llm_max_tokens: int
    llm_explain_max_tokens: int
    llm_review_max_tokens: int
    LLM_API_KEY: str
    LLM_MODEL: str
    LLM_BASE_URL: str

    ALLOWED_ORIGINS: list[str] = []
    

    email_host: str
    email_port: int = 587
    email_username: str
    email_password: str
    email_from: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

# Read .env once and cache the settings for future use
@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()