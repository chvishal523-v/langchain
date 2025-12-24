from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser

from llm_factory import build_llm
from prompts import SUMMARIZE_PROMPT, BULLETS_PROMPT, REWRITE_PROMPT


def summarize(text: str, provider: str = "gemini", mode: str | None = None) -> str:
    llm = build_llm(provider=provider, mode=mode)
    chain = SUMMARIZE_PROMPT | llm | StrOutputParser()
    return chain.invoke({"text": text})


def extract_bullets(text: str, provider: str = "gemini", mode: str | None = None) -> str:
    llm = build_llm(provider=provider, mode=mode)
    chain = BULLETS_PROMPT | llm | StrOutputParser()
    return chain.invoke({"text": text})


def rewrite_tone(text: str, tone: str, provider: str = "gemini", mode: str | None = None) -> str:
    llm = build_llm(provider=provider, mode=mode)
    chain = REWRITE_PROMPT | llm | StrOutputParser()
    return chain.invoke({"text": text, "tone": tone})
