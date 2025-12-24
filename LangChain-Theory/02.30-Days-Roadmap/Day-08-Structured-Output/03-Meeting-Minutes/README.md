# Day 8 — Structured Output (Pydantic-first)
## Meeting Minutes Extraction (meeting_minutes.py)

This mini-demo converts messy meeting notes into **structured JSON** using:
- **LangChain** + (Gemini or Mistral)
- **Pydantic schema** (`MeetingMinutes`)
- A shared helper (`extract_structured`) that asks the LLM to return valid JSON that matches your schema.

---

## What you will build

You will run a script that:
1. Takes meeting text (default included, or pass your own with `--text`)
2. Sends it to an LLM
3. Receives a JSON answer
4. Validates it with Pydantic
5. Prints:
   - `RAW` model output
   - clean validated `JSON`

---

## Folder structure (recommended)

Put these files inside your project like this:

```text
Lang-Chain-30days/
  .env
  day8/
    meeting_minutes.py
    common.py
    schemas.py
    llm_factory.py
    settings.py
```

> This README focuses on `meeting_minutes.py`, but it depends on `common.py`, `schemas.py`, `llm_factory.py`, and `settings.py` from Day 8.

---

## Prerequisites

### 1) Python + Virtual env
- Python **3.10+** recommended
- Create/activate a venv:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

### 2) Install packages

```bash
pip install -U langchain langchain-core python-dotenv pydantic pydantic-settings
pip install -U langchain-google-genai langchain-mistralai
pip install "pydantic[email]"
```

### 3) Create `.env` (API keys)

Create a `.env` file in the project root (same level as `day8/`):

```env
# Gemini
GOOGLE_API_KEY=YOUR_GEMINI_KEY

# Mistral
MISTRAL_API_KEY=YOUR_MISTRAL_KEY
```

> If you only want to run Gemini, you can skip `MISTRAL_API_KEY`, and vice-versa.

---

## How to run

### Run with default meeting text (built-in)
From the project root:

```bash
python .\day8\meeting_minutes.py --provider gemini
```

Or:

```bash
python .\day8\meeting_minutes.py --provider mistral
```

### Run with your own meeting text
Use `--text`:

```bash
python .\day8\meeting_minutes.py --provider gemini --text "Daily Standup. Attendees: Vinay, Rahul. Decisions: ship v1 Friday. Actions: Rahul fix login bug by Thu."
```

---

## Expected output

You will see two sections:

1) **RAW**: whatever the model returned  
2) **JSON**: validated Pydantic output (pretty-printed)

Example:

```text
RAW: (model output)

JSON:
{
  "meeting_title": "...",
  "date": "...",
  "attendees": [...],
  "key_points": [...],
  "decisions": [...],
  "action_items": [
    {"owner":"...", "task":"...", "due_date":"..."}
  ]
}
```

---

## Code (copy-paste)

### `day8/meeting_minutes.py`

```python
import argparse

from schemas import MeetingMinutes
from common import extract_structured

DEFAULT_TEXT = """
Sprint Planning Meeting — Dec 24
Attendees: Vinay, Rahul, Asha

Decision: freeze scope, only bug fixes.
Key points: improve caching, update docs, verify billing flow.

Action items:
- Vinay will prepare release notes by Dec 26.
- Asha will verify billing flow by Dec 25.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", default="gemini", choices=["gemini", "mistral"])
    ap.add_argument("--text", default=DEFAULT_TEXT)
    args = ap.parse_args()

    parsed, raw = extract_structured(
        provider=args.provider,
        schema=MeetingMinutes,
        task_instruction="Convert this text into structured meeting minutes.",
        text=args.text,
        temperature=0.0,
    )

    print("\nRAW:\n", raw)
    print("\nJSON:\n", parsed.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
```

---

## What each part does (simple explanation)

- `MeetingMinutes` (Pydantic schema): defines what the final JSON **must** contain.
- `extract_structured(...)`:
  - sends instructions + your text to the model
  - forces the response to match your schema
  - validates with Pydantic
- `temperature=0.0`:
  - makes output more consistent (less random)
  - important for “data extraction” tasks

---

## Common issues + fixes

### 1) “API key required”
Make sure `.env` exists in the project root and contains:

- `GOOGLE_API_KEY=...` for Gemini
- `MISTRAL_API_KEY=...` for Mistral

Then restart the terminal and run again.

### 2) “JSON invalid” / ValidationError
This means the model returned something that doesn’t match the schema.
Fixes:
- Keep `temperature=0.0`
- Make your meeting text more explicit (add dates, owners, bullet points)
- Re-run (LLMs can be slightly variable)

### 3) Import errors (schemas/common not found)
Run from the project root:

```bash
python .\day8\meeting_minutes.py --provider gemini
```

Not from inside `day8/` unless your Python path is configured.

---

## Screenshots

- Code view: `images/01-meeting_minutes-code.png`
- Terminal output: `images/02-meeting_minutes-output.png`
