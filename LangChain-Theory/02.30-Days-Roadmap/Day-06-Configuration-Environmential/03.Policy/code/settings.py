
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # reads from .env automatically
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # API keys (names match .env)
    google_api_key: str | None = None
    mistral_api_key: str | None = None

    # model defaults
    default_provider: str = "gemini"
    gemini_model: str = "gemini-2.5-flash"
    mistral_model: str = "mistral-large-latest"
    temperature: float = 0.2
    

    app_env: str = "dev"

    
    timeout_sec: int = 60
    max_retries: int = 3
    max_tokens: int = 256


settings = Settings()
