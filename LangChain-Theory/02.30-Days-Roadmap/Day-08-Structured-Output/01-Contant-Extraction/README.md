# Day 8 — Structured Output (Pydantic-first) — Contact Extraction (LangChain)

This mini-project shows how to force **structured JSON output** from an LLM using **Pydantic schemas** and LangChain’s **`PydanticOutputParser`**.

You will run a script (`contact.py`) that extracts a contact from plain text and prints:

- **RAW** model output (JSON text)
- **JSON** (pretty printed) after parsing/validation

---

## What you build today

✅ **Pydantic schema** for a `Contact`  
✅ **LangChain prompt + parser** that tells the LLM the exact JSON format  
✅ **Retry + cleanup fallback** for messy outputs (markdown fences, extra text, etc.)  
✅ A runnable command:

```bash
python day8/contact.py --provider gemini
```

---

## Folder structure

Your project looks like this:

```text
Lang-Chain-30days/
  day8/
    contact.py
    common.py
    schemas.py
    llm_factory.py
    settings.py
  .env
```

---

## Prerequisites

### 1) Python + virtual environment
- Python **3.10+** recommended
- A virtual environment (`.venv`) activated

### 2) API keys
You need at least **one** provider key:

- **Gemini**: `GOOGLE_API_KEY` (or `GEMINI_API_KEY`)
- **Mistral**: `MISTRAL_API_KEY`

Create a `.env` file in the project root (same level as `day8/`):

```env
# Use at least ONE
GOOGLE_API_KEY="PASTE_YOUR_GEMINI_KEY"
# MISTRAL_API_KEY="PASTE_YOUR_MISTRAL_KEY"
```

> Tip (Windows): After editing `.env`, re-open your terminal if variables don’t load.

### 3) Install dependencies

From the project root:

```bash
pip install -U langchain langchain-core pydantic pydantic-settings python-dotenv
pip install -U langchain-google-genai langchain-mistralai
pip install "pydantic[email]"
```

Why `pydantic[email]`?  
It installs the email validator used by `EmailStr`.

---

## Run the demo (Contact Extraction)

### Option A — run from project root (recommended)

```bash
python day8/contact.py --provider gemini
```

Or:

```bash
python day8/contact.py --provider mistral
```

### Option B — run inside the day8 folder

```bash
cd day8
python contact.py --provider gemini
```

> Note: `settings.py` loads `.env` from your **current working directory**.
> If you `cd day8`, either copy `.env` into `day8/` **or** set `GOOGLE_API_KEY` / `MISTRAL_API_KEY` in your shell.


---

## Expected output

You should see **RAW** JSON, then the validated parsed JSON:

```text
RAW:
{"name":"John Doe","email":"john.doe@botcampus.ai","phone":"+91-98765-43210","company":"BotCampusAI"}

JSON:
{
  "name": "John Doe",
  "email": "john.doe@botcampus.ai",
  "phone": "+91-98765-43210",
  "company": "BotCampusAI"
}
```

Screenshot from your run:

![Contact extraction output](images/01-contact-output.png)

---

## How it works (simple explanation)

### 1) Pydantic schema = the “contract”
In `schemas.py`, the `Contact` model defines the shape of the final JSON:

- `name` (string)
- `email` (validated email)
- `phone` (string)
- `company` (string)

If the model returns the wrong shape, Pydantic will throw an error — and you’ll know immediately.

### 2) PydanticOutputParser generates format instructions
LangChain can create **format instructions** automatically from the schema.

Those instructions are injected into the prompt so the model knows exactly what to return.

### 3) The chain is: Prompt → LLM → String
We send the prompt to the model and collect text output:

```python
chain = prompt | llm | StrOutputParser()
```

### 4) `safe_invoke()` retries and cleans JSON
Models sometimes return:

- Markdown fences (```json ...)
- Extra explanation text
- Broken JSON

So `safe_invoke()` does:

1. Call the model
2. Try parse → if success: done
3. If parse fails:
   - clean the text (remove fences, keep JSON block)
   - parse again
4. Retry the model call a few times if needed

---

## Copy‑paste code (Day 8)

> Place these files under `day8/` (and keep `.env` in the project root).



## `day8/settings.py`

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


## `day8/llm_factory.py`

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


## `day8/schemas.py`

```python
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, EmailStr, conint, confloat

# 1) Contact Extraction
class Contact(BaseModel):
    name: str = Field(..., description="Full name")
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None

# 2) Job Posting Extraction
class JobPosting(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    employment_type: Optional[Literal["full-time","part-time","contract","internship","temporary"]] = None
    experience_years: Optional[int] = None
    skills: List[str] = Field(default_factory=list)
    salary_range: Optional[str] = None
    description: Optional[str] = None

# 3) Meeting Minutes (nested)
class ActionItem(BaseModel):
    owner: str
    task: str
    due_date: Optional[str] = None

class MeetingMinutes(BaseModel):
    meeting_title: str
    date: Optional[str] = None
    attendees: List[str] = Field(default_factory=list)
    key_points: List[str] = Field(default_factory=list)
    decisions: List[str] = Field(default_factory=list)
    action_items: List[ActionItem] = Field(default_factory=list)

# 4) Product Review JSON (validation)
class ProductReview(BaseModel):
    product_name: str
    rating: conint(ge=1, le=5)
    sentiment: Literal["positive", "neutral", "negative"]
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)
    summary: str
    would_recommend: bool

# 5) Ticket Triage (enums + confidence)
class TicketTriage(BaseModel):
    customer_name: Optional[str] = None
    issue: str
    category: Literal["billing", "bug", "feature_request", "account", "other"]
    urgency: Literal["low", "medium", "high"]
    recommended_team: Literal["support", "engineering", "billing"]
    suggested_reply: str
    confidence: confloat(ge=0, le=1)
```


## `day8/common.py`

```python
import re
from typing import Any, Dict, Tuple, Type

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.runnables import Runnable

from llm_factory import build_llm

def clean_for_json(text: str) -> str:
    s = (text or "").strip()

    # remove markdown fences
    s = re.sub(r"^```(?:json)?\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"```$", "", s, flags=re.IGNORECASE).strip()

    # keep only first JSON object block
    first = s.find("{")
    last = s.rfind("}")
    if first != -1 and last != -1 and last > first:
        s = s[first:last+1]

    return s.strip()

def safe_invoke(chain: Runnable, inputs: Dict[str, Any], parser: PydanticOutputParser, max_attempts: int = 3):
    last_raw = ""
    for _ in range(max_attempts):
        last_raw = chain.invoke(inputs)

        # try direct parse
        try:
            return parser.parse(last_raw), last_raw
        except Exception:
            # try cleaned parse
            cleaned = clean_for_json(last_raw)
            return parser.parse(cleaned), last_raw

    raise RuntimeError("safe_invoke failed")

def extract_structured(
    provider: str,
    schema: Type[Any],
    task_instruction: str,
    text: str,
    temperature: float = 0.0,
    max_attempts: int = 3
) -> Tuple[Any, str]:

    parser = PydanticOutputParser(pydantic_object=schema)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Return ONLY valid JSON. No markdown. No extra text."),
        ("human",
         "{task}\n\nFORMAT RULES:\n{format_instructions}\n\nTEXT:\n{text}")
    ])

    llm = build_llm(provider=provider, temperature=temperature)
    chain = prompt | llm | StrOutputParser()

    return safe_invoke(chain, {
        "task": task_instruction,
        "format_instructions": parser.get_format_instructions(),
        "text": text
    }, parser, max_attempts=max_attempts)
```


## `day8/contact.py`

```python
import argparse
from schemas import Contact
from common import extract_structured

DEFAULT_TEXT = """
Hey! This is John Doe from BotCampusAI.
You can reach me at john.doe@botcampus.ai or +91-98765-43210.
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", default="gemini", choices=["gemini","mistral"])
    ap.add_argument("--text", default=DEFAULT_TEXT)
    args = ap.parse_args()

    parsed, raw = extract_structured(
        provider=args.provider,
        schema=Contact,
        task_instruction="Extract contact details from the text.",
        text=args.text,
        temperature=0.0,
    )

    print("\nRAW:\n", raw)
    print("\nJSON:\n", parsed.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
```

---

## Common issues

### “API key required…” (Gemini / Mistral)
Make sure your `.env` has the key **and** you’re running from the project root.

✅ `.env` must be in: `Lang-Chain-30days/.env`  
✅ Script should be run like: `python day8/contact.py --provider gemini`

### Email validation error
If you see errors related to email validation, install:

```bash
pip install "pydantic[email]"
```

---

## Next steps (to cover the full Day 8 theme)

This “Contact extraction” script is the base pattern.

To add the other Day 8 structured outputs, you repeat the same pattern:

1. Create a new Pydantic schema in `schemas.py`
2. Create a new script (example: `job_posting.py`)
3. Call `extract_structured(...)` with the schema + task instruction

Targets you can implement next:
- Job posting extraction
- Meeting minutes extraction
- Product review JSON
- Ticket triage
