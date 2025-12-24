from dotenv import load_dotenv
#from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_mistralai import ChatMistralAI


load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert rewriter. Preserve meaning. No new facts."),
    ("human",
     "Rewrite the text.\n"
     "Tone: {tone}\n"
     "Audience: {audience}\n"
     "Length: {length}\n"
     "Format: {format}\n\n"
     "TEXT:\n{text}"
    )
])
llm = ChatMistralAI(model="mistral-large-latest", temperature=0.5)
#llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)
parser = StrOutputParser()

chain = prompt | llm | parser

# --- A) Normal invoke ---
text = "LangChain helps build LLM apps. It has prompts, chains, retrieval, and agents."
out = chain.invoke({
    "text": text,
    "tone": "professional",
    "audience": "beginners",
    "length": "short",
    "format": "markdown paragraph"
})
print("\nINVOKE OUTPUT:\n", out)

# --- B) Batch (multiple rewrites in one go) ---
batch_inputs = [
    {"text": text, "tone": "friendly", "audience": "kids", "length": "short", "format": "simple paragraph"},
    {"text": text, "tone": "formal", "audience": "managers", "length": "medium", "format": "bullet points"},
]
batch_out = chain.batch(batch_inputs)
print("\nBATCH OUTPUT:\n", batch_out)

# --- C) Streaming (prints chunks as they arrive) ---
print("\nSTREAM OUTPUT:\n", end="")
for chunk in chain.stream({
    "text": text,
    "tone": "professional",
    "audience": "beginners",
    "length": "short",
    "format": "markdown paragraph"
}):
    print(chunk, end="")
print()
