import os
import time
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI

load_dotenv()

PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Stream your answer."),
    ("human", "Write EXACTLY 120 words about: {topic}")
])

def stream_once(model_name: str, chain, inputs: dict):
    print(f"\n\n===== {model_name} (STREAM) =====")
    start = time.perf_counter()
    first_chunk_time = None

    text_parts = []
    for chunk in chain.stream(inputs):
        if first_chunk_time is None:
            first_chunk_time = time.perf_counter()
        print(chunk, end="", flush=True)
        text_parts.append(chunk)

    end = time.perf_counter()
    full_text = "".join(text_parts)

    ttft = (first_chunk_time - start) if first_chunk_time else None
    print("\n\n--- METRICS ---")
    print(f"TTFT (time to first chunk): {ttft:.3f}s" if ttft is not None else "TTFT: N/A")
    print(f"Total time: {end - start:.3f}s")
    print(f"Chars: {len(full_text)}")

def main():
    parser = StrOutputParser()

    gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)
    mistral = ChatMistralAI(model="mistral-large-latest", temperature=0.0)

    gemini_chain = PROMPT | gemini | parser
    mistral_chain = PROMPT | mistral | parser

    inputs = {"topic": "LangChain LCEL and why streaming matters"}

    stream_once("Gemini", gemini_chain, inputs)
    stream_once("Mistral", mistral_chain, inputs)

if __name__ == "__main__":
    main()
