from settings import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI

def build_llm(provider: str | None = None, temperature: float | None = None):
    provider = (provider or settings.default_provider).lower()
    temp = settings.temperature if temperature is None else temperature

    if provider == "gemini":
        if not settings.google_api_key:
            raise ValueError("Missing GOOGLE_API_KEY in .env")
        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            temperature=temp,
            max_retries=settings.max_retries,
            timeout=settings.timeout_sec,
            max_output_tokens=settings.max_tokens,
            api_key=settings.google_api_key,
        )

    if provider == "mistral":
        if not settings.mistral_api_key:
            raise ValueError("Missing MISTRAL_API_KEY in .env")
        return ChatMistralAI(
            model=settings.mistral_model,
            temperature=temp,
            max_retries=settings.max_retries,
            timeout=settings.timeout_sec,
            max_tokens=settings.max_tokens,
            api_key=settings.mistral_api_key,
        )

    raise ValueError("provider must be 'gemini' or 'mistral'")
