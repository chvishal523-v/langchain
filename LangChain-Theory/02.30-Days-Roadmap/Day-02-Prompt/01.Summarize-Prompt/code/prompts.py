
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


