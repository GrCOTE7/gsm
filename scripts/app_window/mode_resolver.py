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

    # Modes internes (fenêtres CLI dédiées lancées par cli_spawner) :
    # format "_<app>_child[_<mode>]" (ex: _gsm_child, _gsm_child_web).
    # Le processus enfant relaie l'application demandée, MAIS ne doit pas
    # rouvrir une nouvelle CLI (sinon récursion infinie de fenêtres).
    # Variante "_<app>_nocli[_<mode>]" : enfant détaché en mode multi-apps
    # SANS CLI dédiée (./go gu) — ne repositionne aucune console.
    if mode.startswith("_"):
        parts = mode[1:].split("_")
        app_name = parts[0] if parts and parts[0] in ("gsm", "upu") else "gsm"
        child_mode = (
            parts[2] if len(parts) > 2 and parts[2] in ("app", "web") else "app"
        )
        return {
            "apps": [app_name],
            "mode": child_mode,
            "internal_child": True,
            # Seule la vraie CLI dédiée repositionne sa console.
            "skip_cli_placement": len(parts) > 1 and parts[1] != "child",
        }

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
