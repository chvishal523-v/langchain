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
