import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You extract information and output ONLY valid JSON."),
    ("human",
     "Extract the following fields from the text:\n"
     "- name\n- issue\n- urgency (low/medium/high)\n\n"
     "Return JSON with exactly these keys.\n\n"
     "TEXT:\n{text}"
    )
])

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)

parser = JsonOutputParser()

chain = prompt | llm | parser

text = "Hi, I'm James. Your app is charging me twice every month. This is urgent."
data = chain.invoke({"text": text})

print(data)          # dict
print(data["issue"]) # example access
