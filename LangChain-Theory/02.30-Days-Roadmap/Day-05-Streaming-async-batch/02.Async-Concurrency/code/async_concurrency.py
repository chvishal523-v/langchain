import asyncio
import time
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI

load_dotenv()

PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "Give 3 bullet points about: {topic}")
])

async def run_sequential(chain, topics):
    start = time.perf_counter()
    results = []
    for t in topics:
        out = await chain.ainvoke({"topic": t})
        results.append(out)
    end = time.perf_counter()
    return results, end - start

async def run_concurrent(chain, topics):
    start = time.perf_counter()
    tasks = [chain.ainvoke({"topic": t}) for t in topics]
    results = await asyncio.gather(*tasks)
    end = time.perf_counter()
    return results, end - start

async def bench(model_name, chain):
    topics = [
        "RAG vs fine-tuning",
        "What is LCEL?",
        "Token streaming use-cases",
        "Async in Python for LLM apps",
        "Batching requests"
    ]

    seq_out, seq_time = await run_sequential(chain, topics)
    con_out, con_time = await run_concurrent(chain, topics)

    print(f"\n===== {model_name} (ASYNC BENCH) =====")
    print(f"Sequential time: {seq_time:.3f}s")
    print(f"Concurrent time: {con_time:.3f}s")
    print(f"Speedup: {seq_time / con_time:.2f}x" if con_time > 0 else "Speedup: N/A")

async def main():
    parser = StrOutputParser()

    gemini = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.0)
    mistral = ChatMistralAI(model="mistral-large-latest", temperature=0.0)

    gemini_chain = PROMPT | gemini | parser
    mistral_chain = PROMPT | mistral | parser

    await bench("Gemini", gemini_chain)
    await bench("Mistral", mistral_chain)

if __name__ == "__main__":
    asyncio.run(main())
