from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    google_api_key: str | None = None
    mistral_api_key: str | None = None

    default_provider: str = "gemini"
    gemini_model: str = "gemini-2.5-flash"
    mistral_model: str = "mistral-large-latest"

    timeout_sec: int = 60
    max_retries: int = 3
    temperature: float = 0.2
    max_tokens: int = 512

settings = Settings()
