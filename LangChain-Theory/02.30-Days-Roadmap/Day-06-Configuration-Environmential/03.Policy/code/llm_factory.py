from settings import settings
from policy import temperature_for

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI

def build_llm(provider: str | None = None, mode: str = "balanced"):
    provider = (provider or settings.default_provider).lower()
    temp = temperature_for(mode)

    if provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            temperature=temp,
            max_retries=settings.max_retries,
            timeout=settings.timeout_sec,
            max_output_tokens=settings.max_tokens,
            api_key=settings.google_api_key,
        )

    if provider == "mistral":
        return ChatMistralAI(
            model=settings.mistral_model,
            temperature=temp,
            max_retries=settings.max_retries,
            timeout=settings.timeout_sec,
            max_tokens=settings.max_tokens,
            api_key=settings.mistral_api_key,
        )

    raise ValueError(f"Unknown provider: {provider}")
