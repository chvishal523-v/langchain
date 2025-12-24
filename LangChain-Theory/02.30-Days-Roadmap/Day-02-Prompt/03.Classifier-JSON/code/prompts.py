
from langchain_core.prompts import ChatPromptTemplate

SUMMARIZER_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a professional summarizer. "
     "Follow the instructions exactly."),
    ("human",
     "Summarize the text below.\n\n"
     "RULES:\n"
     "- Output must be bullet points only\n"
     "- Max {max_bullets} bullets\n"
     "- Each bullet <= 18 words\n"
     "- No extra commentary\n\n"
     "TEXT:\n"
     "```{text}```"
    )
])

REWRITER_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are an expert rewriter. You must preserve meaning, "
     "but improve clarity and structure. Follow instructions exactly."),
    ("human",
     "Rewrite the text below.\n\n"
     "SETTINGS:\n"
     "- Tone: {tone}\n"
     "- Audience: {audience}\n"
     "- Length: {length}\n"
     "- Output format: {format}\n\n"
     "RULES:\n"
     "- Do not add new facts\n"
     "- Do not remove key details\n"
     "- No meta text like 'Here is the rewrite'\n\n"
     "TEXT:\n```{text}```"
    )
])

CLASSIFIER_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a strict classifier.\n"
     "You must output ONLY valid JSON.\n"
     "No markdown, no explanations outside JSON."),
    ("human",
     "Classify the text into EXACTLY ONE label from this list:\n"
     "{labels}\n\n"
     "Return JSON EXACTLY like:\n"
     "{{\"label\":\"<one label>\",\"confidence\":0.0,\"reason\":\"short reason\"}}\n\n"
     "TEXT:\n```{text}```"
    )
])

def format_labels(labels: list[str]) -> str:
    # helps keep labels consistent and readable
    return "\\n".join([f"- {x}" for x in labels])