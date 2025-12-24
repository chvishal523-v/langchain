from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized config loaded from `.env` (and system env vars)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # API keys
    google_api_key: str | None = None  # GOOGLE_API_KEY
    gemini_api_key: str | None = None  # GEMINI_API_KEY
    mistral_api_key: str | None = None  # MISTRAL_API_KEY

    # model defaults
    default_provider: str = "gemini"
    gemini_model: str = "gemini-2.5-flash"
    mistral_model: str = "mistral-large-latest"

    # policies
    temperature: float = 0.2
    timeout_sec: int = 60
    max_retries: int = 3
    max_tokens: int = 256


settings = Settings()
