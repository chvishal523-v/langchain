from settings import settings

def temperature_for(mode: str = "balanced") -> float:
    # If you want prod to always be stable:
    # if settings.app_env == "prod": return 0.0

    mode = (mode or "balanced").lower()

    if mode == "deterministic":
        return 0.0
    if mode == "balanced":
        return 0.2
    if mode == "creative":
        return 0.8

    return settings.temperature
