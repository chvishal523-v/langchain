# Day 7 — Mini Project #1: Content Assistant (CLI)

A clean **command-line app** built with **LangChain** that supports 3 commands:

- `summarize` — short summary of input text
- `bullets` — extract bullet points
- `rewrite` — rewrite the text in a specific tone

It works with **Gemini** or **Mistral** (choose using `--provider`).

---

## 1) What you will build

You will run commands like these:

```bash
# Summarize
python day7/cli.py summarize --text "LangChain helps you build LLM apps faster..."

# Extract bullets
python day7/cli.py bullets --text "LangChain is useful for RAG, agents, and production apps..."

# Rewrite with a tone
python day7/cli.py rewrite --text "Launch our product" --tone funny --mode creative
```

---

## 2) Prerequisites (required)

### System
- Python **3.10+** (recommended: 3.11 or 3.12)
- Internet connection (model APIs are cloud)

### API Keys
You need at least one:

**Gemini**
- `GOOGLE_API_KEY` or `GEMINI_API_KEY`

**Mistral**
- `MISTRAL_API_KEY`

### Python packages
Install these in a virtual environment:

- `langchain`
- `langchain-core`
- `langchain-google-genai`
- `langchain-mistralai`
- `pydantic-settings`
- `python-dotenv`

---

## 3) Project setup (step-by-step)

> These steps assume your project root folder is `Lang-Chain-30days/`.

### Step A — Create a virtual environment (Windows PowerShell)
```powershell
cd C:\Users\Vinay\OneDrive\Desktop\Lang-Chain-30days
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step B — Install dependencies
```powershell
pip install -U langchain langchain-core langchain-google-genai langchain-mistralai pydantic-settings python-dotenv
```

### Step C — Create `.env` in the project root
Create a file:

```
Lang-Chain-30days/.env
```

Example `.env`:

```env
# Pick one or both providers

# Gemini
GOOGLE_API_KEY=your_google_api_key_here
# (optional alternative name)
GEMINI_API_KEY=your_gemini_api_key_here

# Mistral
MISTRAL_API_KEY=your_mistral_api_key_here
```

### Step D — Place the code files in `day7/`
Create this folder if it does not exist:

```
Lang-Chain-30days/day7/
```

Put these files inside it:

- `cli.py`
- `content_service.py`
- `llm_factory.py`
- `prompts.py`
- `settings.py`

Your structure should look like:

```
Lang-Chain-30days/
  .env
  day7/
    cli.py
    content_service.py
    llm_factory.py
    prompts.py
    settings.py
```

---

## 4) Run the CLI

### 4.1 Show help
```bash
python day7/cli.py -h
```

### 4.2 Summarize
```bash
python day7/cli.py summarize --text "LangChain helps you build LLM apps faster..."
```

### 4.3 Extract bullets
```bash
python day7/cli.py bullets --text "LangChain is useful for RAG, agents, and production apps. It also supports multiple providers."
```

### 4.4 Rewrite tone
```bash
python day7/cli.py rewrite --text "Launch our product" --tone "funny" --mode creative
```

---

## 5) CLI options (important)

### Providers
- `--provider gemini` (default)
- `--provider mistral`

Example:
```bash
python day7/cli.py summarize --provider mistral --text "..."
```

### Temperature / creativity modes
- `--mode deterministic` → temperature = 0.0 (most stable)
- `--mode balanced` → temperature = 0.2 (default)
- `--mode creative` → temperature = 0.8 (more creative)

Example:
```bash
python day7/cli.py rewrite --mode deterministic --tone "professional" --text "..."
```

---

## 6) Common errors + fixes

### Error: `the following arguments are required: command`
You ran only:

```bash
python day7/cli.py
```

But you must add a command (`summarize`, `bullets`, or `rewrite`):

```bash
python day7/cli.py summarize --text "Hello"
```

### Error: `can't open file ... day7\cli.py: [Errno 2] No such file or directory`
The path is wrong or `day7/cli.py` is not there.

1) Check folder:
```powershell
dir day7
```

2) Run from the project root:
```powershell
cd C:\Users\Vinay\OneDrive\Desktop\Lang-Chain-30days
python day7\cli.py -h
```

### Error: `API key required ... set GOOGLE_API_KEY/GEMINI_API_KEY`
Your `.env` is missing keys or not being loaded.

1) Confirm `.env` exists at project root.
2) Put keys in `.env`:
```env
GOOGLE_API_KEY=xxxx
MISTRAL_API_KEY=yyyy
```
3) Re-run:
```bash
python day7/cli.py summarize --provider gemini --text "test"
```

---

## 7) How the code works (brief)

- `settings.py`  
  Uses **Pydantic Settings** to load configuration from `.env`:
  API keys, default provider, model names, timeout, retries, and max tokens.

- `llm_factory.py`  
  Creates the correct LangChain chat model based on `--provider` and `--mode`.
  Also applies retry/timeout/max token settings.

- `prompts.py`  
  Stores prompt templates for summarize / bullets / rewrite.

- `content_service.py`  
  Contains helper functions that run the selected chain and return output text.

- `cli.py`  
  The main entry point. Uses `argparse` subcommands:
  `summarize`, `bullets`, `rewrite`.

---

## 8) Full code (copy‑paste)

> Put each file below into `Lang-Chain-30days/day7/` with the same name.

### `settings.py`
```python
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
```

### `llm_factory.py`
```python
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
```

### `prompts.py`
```python
from langchain_core.prompts import ChatPromptTemplate

SUMMARIZE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Return only the answer (no markdown)."),
    ("human", "Summarize the text in 3–4 short sentences:\n\n{text}"),
])

BULLETS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Return only the answer (no markdown)."),
    ("human", "Extract 5 concise bullet points from the text:\n\n{text}"),
])

REWRITE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Return only the answer (no markdown)."),
    ("human", "Rewrite the text in a {tone} tone. Keep meaning same:\n\n{text}"),
])
```

### `content_service.py`
```python
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
```

### `cli.py`
```python
from __future__ import annotations

import argparse
from pathlib import Path

from content_service import summarize, extract_bullets, rewrite_tone


def read_text(args) -> str:
    if args.text:
        return args.text.strip()

    if args.file:
        p = Path(args.file)
        if not p.exists():
            raise FileNotFoundError(f"File not found: {p}")
        return p.read_text(encoding="utf-8").strip()

    raise ValueError("Provide --text or --file")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="content-assistant",
        description="Day 7: LangChain Content Assistant CLI (summarize / bullets / rewrite)"
    )

    parser.add_argument(
        "--provider",
        default="gemini",
        choices=["gemini", "mistral"],
        help="Which model provider to use (default: gemini)"
    )

    parser.add_argument(
        "--mode",
        default="balanced",
        choices=["deterministic", "balanced", "creative"],
        help="Temperature policy mode (default: balanced)"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_sum = sub.add_parser("summarize", help="Summarize text (3–4 sentences)")
    p_sum.add_argument("--text", help="Input text")
    p_sum.add_argument("--file", help="Path to a .txt file")

    p_bul = sub.add_parser("bullets", help="Extract 5 bullet points")
    p_bul.add_argument("--text", help="Input text")
    p_bul.add_argument("--file", help="Path to a .txt file")

    p_rew = sub.add_parser("rewrite", help="Rewrite in a chosen tone")
    p_rew.add_argument("--tone", required=True, help="Tone (e.g., professional, casual, funny)")
    p_rew.add_argument("--text", help="Input text")
    p_rew.add_argument("--file", help="Path to a .txt file")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    text = read_text(args)

    if args.command == "summarize":
        out = summarize(text=text, provider=args.provider, mode=args.mode)
    elif args.command == "bullets":
        out = extract_bullets(text=text, provider=args.provider, mode=args.mode)
    elif args.command == "rewrite":
        out = rewrite_tone(text=text, tone=args.tone, provider=args.provider, mode=args.mode)
    else:
        raise ValueError("Unknown command")

    print("\n===== OUTPUT =====\n")
    print(out)


if __name__ == "__main__":
    main()
```
