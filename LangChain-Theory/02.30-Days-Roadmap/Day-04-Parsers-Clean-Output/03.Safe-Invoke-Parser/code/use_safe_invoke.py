from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from schemas import Ticket
from safe_invoke import safe_invoke

load_dotenv()

parser = PydanticOutputParser(pydantic_object=Ticket)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Return ONLY JSON. No markdown. No extra text."),
    ("human",
     "Extract a support ticket.\n"
     "FORMAT RULES:\n{format_instructions}\n\n"
     "TEXT:\n{text}")
])

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)

# chain returns string (important for safe_invoke)
chain = prompt | llm | StrOutputParser()

result, raw = safe_invoke(
    chain,
    {
        "text": "Hi I'm James. Your app is charging me twice every month. This is urgent.",
        "format_instructions": parser.get_format_instructions()
    },
    parser,
    max_attempts=3
)

print("RAW:\n", raw)
print("PARSED:\n", result)
