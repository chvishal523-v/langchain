from typing import Any, Dict, Optional, Tuple
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import BaseOutputParser
from parse_fallback import clean_for_json

def safe_invoke(
    chain: Runnable,
    inputs: Dict[str, Any],
    parser: BaseOutputParser,
    *,
    max_attempts: int = 3
) -> Tuple[Any, str]:
    """
    Runs a chain safely and returns:
      (parsed_result, raw_text)

    Requirements:
    - `chain` should return a STRING (use StrOutputParser at end)
    - `parser` is a PydanticOutputParser or JsonOutputParser

    Strategy:
    - Attempt parse
    - If fail: clean_for_json() then parse again
    - Retry the whole model call up to max_attempts
    """
    last_err: Optional[Exception] = None
    last_raw: str = ""

    for attempt in range(1, max_attempts + 1):
        try:
            last_raw = chain.invoke(inputs)

            # 1) direct parse
            try:
                return parser.parse(last_raw), last_raw
            except Exception:
                # 2) fallback clean + parse
                cleaned = clean_for_json(last_raw)
                return parser.parse(cleaned), last_raw

        except Exception as e:
            last_err = e

    raise RuntimeError(f"safe_invoke failed after {max_attempts} attempts. Last error: {last_err}\nLast raw:\n{last_raw}")
