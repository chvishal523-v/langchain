
from settings import settings

def main():
    print("✅ Loaded Settings:")
    print("default_provider:", settings.default_provider)
    print("gemini_model:", settings.gemini_model)
    print("mistral_model:", settings.mistral_model)
    print("temperature:", settings.temperature)

    print("google_api_key set?:", bool(settings.google_api_key))
    print("mistral_api_key set?:", bool(settings.mistral_api_key))

if __name__ == "__main__":
    main()
