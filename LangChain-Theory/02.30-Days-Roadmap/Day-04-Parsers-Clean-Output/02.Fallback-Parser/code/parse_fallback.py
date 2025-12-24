import re

def strip_code_fences(text: str) -> str:
    """Removes ```json ... ``` fences if present."""
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else text

def extract_first_json_object(text: str) -> str:
    """
    Best-effort: find first '{' and last '}' to salvage JSON object.
    Works when model adds extra text before/after JSON.
    """
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start:end+1].strip()
    return text

def clean_for_json(text: str) -> str:
    text = strip_code_fences(text)
    text = extract_first_json_object(text)
    return text
