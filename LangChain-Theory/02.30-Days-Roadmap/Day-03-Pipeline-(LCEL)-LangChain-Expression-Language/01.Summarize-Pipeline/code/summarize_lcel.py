from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# 1) Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise summarizer. Output bullet points only."),
    ("human", "Summarize this text in max {max_bullets} bullets:\n\n{text}")
])

# 2) Model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

# 3) Parser (converts AIMessage -> string)
parser = StrOutputParser()

# LCEL pipeline: prompt | model | parser
chain = prompt | llm | parser

text = "LangChain helps build LLM apps. It supports prompts, tools, agents, and retrieval."
result = chain.invoke({"text": text, "max_bullets": 4})

print(result)
