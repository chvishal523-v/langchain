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
