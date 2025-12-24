from __future__ import annotations

from dotenv import load_dotenv

from settings import settings

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI


def temperature_for(mode: str | None) -> float:
    """Simple temperature policy."""
    mode = (mode or "balanced").lower()
    if mode == "deterministic":
        return 0.0
    if mode == "balanced":
        return 0.2
    if mode == "creative":
        return 0.8
    return settings.temperature


def build_llm(provider: str | None = None, mode: str | None = None):
    """Create an LLM client (Gemini or Mistral) using env-driven settings."""
    load_dotenv()

    provider = (provider or settings.default_provider).lower()
    temp = temperature_for(mode)

    if provider == "gemini":
        api_key = settings.google_api_key or settings.gemini_api_key
        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            temperature=temp,
            max_retries=settings.max_retries,
            timeout=settings.timeout_sec,
            max_output_tokens=settings.max_tokens,
            api_key=api_key,
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

    raise ValueError(f"Unknown provider: {provider}. Use gemini or mistral.")
