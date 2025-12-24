from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from schemas import Ticket

# Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
# Mistral (optional)
# from langchain_mistralai import ChatMistralAI

load_dotenv()

parser = PydanticOutputParser(pydantic_object=Ticket)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You must follow the format rules exactly."),
    ("human",
     "Extract a support ticket from the text.\n"
     "FORMAT RULES:\n{format_instructions}\n\n"
     "TEXT:\n{text}")
])

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
# llm = ChatMistralAI(model="mistral-large-latest", temperature=0.0)

chain = prompt | llm | parser  # prompt | model | parser ✅

text = "Hi I'm James. Your app is charging me twice every month. This is urgent."
ticket = chain.invoke({"text": text, "format_instructions": parser.get_format_instructions()})

print(ticket)
print(ticket.issue)
