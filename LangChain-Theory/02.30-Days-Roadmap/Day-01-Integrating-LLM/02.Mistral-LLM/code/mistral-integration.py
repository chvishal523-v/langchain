import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv()

llm = ChatMistralAI(
    model=os.getenv("MISTRAL_MODEL", "mistral-large-latest"),
    temperature=0.2,
    max_retries=2,
)

messages = [
    ("system", "You are a concise assistant."),
    ("human", "Explain about Ai in 50 words."),
]

resp = llm.invoke(messages)
print(resp.content)
