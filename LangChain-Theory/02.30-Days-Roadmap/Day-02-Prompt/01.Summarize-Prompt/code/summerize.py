from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts import SUMMARIZER_PROMPT
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

text = input("Enter text to summarize : ")
msg = SUMMARIZER_PROMPT.format_messages(text=text, max_bullets=10)
resp = llm.invoke(msg)
print("Ai: ",resp.content)
