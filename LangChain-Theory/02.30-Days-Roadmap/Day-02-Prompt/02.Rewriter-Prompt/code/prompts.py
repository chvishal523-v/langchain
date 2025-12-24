
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

