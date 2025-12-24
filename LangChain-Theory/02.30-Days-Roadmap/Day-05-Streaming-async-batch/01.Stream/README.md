# Day 5 — Streaming demo (Gemini vs Mistral) + latency metrics
This folder contains a **token streaming** example using LangChain with:
- **Gemini** (`langchain-google-genai`)
- **Mistral** (`langchain-mistralai`)

The script prints tokens as they arrive and also measures:
- **TTFT** = *Time To First Token* (first streamed chunk)
- **Total latency** (full response time)
- Output length (characters)

---

## 1) Folder structure

```text
day5/
  stream_demo.py
  images/
    01.png
    02.png
```

**Screenshots included**
- `images/01.png` → `stream_demo.py` code in VS Code  
- `images/02.png` → terminal output showing Gemini vs Mistral streaming + metrics

---

## 2) Prerequisites

### A) Python
- Python **3.10+** (recommended 3.11 / 3.12)

Check:
```bash
python --version
```

### B) Create & activate a virtual environment
Windows (PowerShell):
```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

macOS / Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```

### C) Install dependencies
```bash
pip install -U langchain langchain-core python-dotenv \
  langchain-google-genai langchain-mistralai
```

### D) Create a `.env` file (IMPORTANT)
In your project root (same level as `day5/`), create:

```env
GOOGLE_API_KEY=your_google_api_key_here
MISTRAL_API_KEY=your_mistral_api_key_here
```

Notes:
- Gemini uses `GOOGLE_API_KEY`
- Mistral uses `MISTRAL_API_KEY`

---

## 3) Copyable code — `day5/stream_demo.py`

```python
import time
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI

load_dotenv()

PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Stream your answer."),
        ("human", "Write EXACTLY 120 words about: {topic}"),
    ]
)

def stream_once(model_name: str, chain, inputs: dict) -> None:
    print(f"\n===== {model_name} (STREAM) =====")

    start = time.perf_counter()
    first_chunk_time = None
    text_parts = []

    for chunk in chain.stream(inputs):
        # Record time-to-first-token (TTFT)
        if first_chunk_time is None:
            first_chunk_time = time.perf_counter()

        print(chunk, end="", flush=True)
        text_parts.append(chunk)

    end = time.perf_counter()
    full_text = "".join(text_parts)

    ttft = (first_chunk_time - start) if first_chunk_time else None

    print("\n\n--- METRICS ---")
    print(f"TTFT (time to first chunk): {ttft:.3f}s" if ttft is not None else "TTFT: N/A")
    print(f"Total time: {end - start:.3f}s")
    print(f"Chars: {len(full_text)}")

def main() -> None:
    parser = StrOutputParser()

    gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)
    mistral = ChatMistralAI(model="mistral-large-latest", temperature=0.0)

    gemini_chain = PROMPT | gemini | parser
    mistral_chain = PROMPT | mistral | parser

    inputs = {"topic": "LangChain LCEL and why streaming matters"}

    stream_once("Gemini", gemini_chain, inputs)
    stream_once("Mistral", mistral_chain, inputs)

if __name__ == "__main__":
    main()

```

---

## 4) Run the demo

From your project root:
```bash
python .\\day5\\stream_demo.py
```

Expected output:
- First it prints **Gemini** output streaming live.
- Then prints **Mistral** output streaming live.
- After each model, you see:

```text
--- METRICS ---
TTFT (time to first chunk): 0.560s
Total time: 5.747s
Chars: 1078
```

---

## 5) How the code works (simple explanation)

### Step 1 — Prompt
`ChatPromptTemplate` creates the system + user message and injects `{topic}`.

### Step 2 — Models
We create one client for Gemini and one for Mistral.

### Step 3 — Parser
`StrOutputParser()` converts the model output to plain text.

### Step 4 — LCEL chain
`PROMPT | model | parser` builds a runnable pipeline.

### Step 5 — Streaming + timing
`chain.stream(inputs)` yields text chunks as they are generated.
We record:
- `start` time
- `first_chunk_time` to calculate TTFT
- `end` time for total latency

---

## 6) Day 5 learning tasks (upgrade path)

### ✅ Task 1 — Stream from one model (basic)
1. Build chain: `PROMPT | gemini | StrOutputParser()`
2. Print: `for chunk in chain.stream(inputs): ...`

### ✅ Task 2 — Two models + TTFT metrics (upgrade of Task 1)
1. Create `stream_once()` helper
2. Run Gemini + Mistral with same prompt and compare TTFT/total

### ✅ Task 3 — Async + batch benchmark (upgrade of Task 2)
1. Use `await chain.ainvoke(...)`
2. Use `asyncio.gather(...)` to run multiple requests concurrently
3. Use `chain.batch([...])` to test throughput
4. Print a small benchmark table:
   `model | mode | avg_ttft | avg_total | chars`

---

## 7) Troubleshooting

### Keys not found
- Ensure `.env` exists and `load_dotenv()` is called.
- Restart terminal after editing `.env`.

### Import errors
Install missing packages:
```bash
pip install -U langchain-google-genai langchain-mistralai
```
