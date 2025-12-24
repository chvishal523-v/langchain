import time
from llm_factory import build_llm

def run(provider: str):
    llm = build_llm(provider)
    prompt = "Write 3 bullet points on why configuration matters in AI apps."

    start = time.perf_counter()
    resp = llm.invoke(prompt)
    end = time.perf_counter()

    print(f"\n===== {provider.upper()} OUTPUT =====")
    print(resp.content)
    print(f"Latency: {end - start:.2f}s")

def main():
    run("gemini")
    run("mistral")

if __name__ == "__main__":
    main()
