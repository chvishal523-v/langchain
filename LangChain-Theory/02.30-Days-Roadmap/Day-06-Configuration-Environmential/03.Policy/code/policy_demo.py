from llm_factory import build_llm

PROMPT = "Give a short slogan for an AI automation tool."

def demo(provider: str):
    det = build_llm(provider, mode="deterministic").invoke(PROMPT).content
    cre = build_llm(provider, mode="creative").invoke(PROMPT).content

    print(f"\n===== {provider.upper()} POLICY DEMO =====")
    print("\n[deterministic]")
    print(det)
    print("\n[creative]")
    print(cre)

def main():
    demo("gemini")
    demo("mistral")

if __name__ == "__main__":
    main()
