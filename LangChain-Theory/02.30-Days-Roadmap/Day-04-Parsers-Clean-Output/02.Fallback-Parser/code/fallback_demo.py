from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from schemas import Ticket
from parse_fallback import clean_for_json

load_dotenv()

parser = PydanticOutputParser(pydantic_object=Ticket)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Return ONLY JSON. No markdown. No extra text."),
    ("human",
     "Extract a ticket.\n"
     "FORMAT RULES:\n{format_instructions}\n\n"
     "TEXT:\n{text}")
])

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)

# We intentionally parse ourselves after cleaning:
chain = prompt | llm | StrOutputParser()

raw = chain.invoke({
    "text": "Hi I'm James. Your app is charging me twice. This is urgent.",
    "format_instructions": parser.get_format_instructions()
})

cleaned = clean_for_json(raw)
ticket = parser.parse(cleaned)

print("RAW:\n", raw)
print("CLEANED:\n", cleaned)
print("PARSED:\n", ticket)
