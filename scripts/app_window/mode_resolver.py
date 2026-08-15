def resolve_mode(mode: str) -> dict:
    """
    Convertit le mode demandé en une structure décrivant
    quelles apps lancer et dans quel mode (app/web).

    Retourne un dict du type :
    {
        "apps": ["gsm", "upu"],
        "mode": "app"  # ou "web"
    }
    """

    mode = mode.lower().strip()

    # ./go → GSM en mode APP
    if mode == "":
        return {"apps": ["gsm"], "mode": "app"}

    # ./go w → GSM en mode WEB
    if mode == "w":
        return {"apps": ["gsm"], "mode": "web"}

    # ./go u → UPU en mode APP
    if mode == "u":
        return {"apps": ["upu"], "mode": "app"}

    # ./go gu → GSM + UPU en mode APP
    if mode == "gu":
        return {"apps": ["gsm", "upu"], "mode": "app"}
    
    if mode == "debug":
        return {"apps": ["gsm"], "mode": "debug"}

    # Fallback : comportement par défaut
    return {"apps": ["gsm"], "mode": "app"}
