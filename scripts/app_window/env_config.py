import os

from dotenv import dotenv_values

from common import ENV_PATH

# Seules ces clés du .env intéressent le launcher (fenêtres / CLI / debug).
LAUNCHER_KEYS = {
    "GSM_WINDOW_LEFT": int,
    "GSM_WINDOW_CLI": int,
    "UPU_WINDOW_LEFT": int,
    "UPU_WINDOW_CLI": int,
    "GSM_DEBUG_RELEASE_JSON": int,
    "ENV_LOCAL": int,
    "DEV": int,
}


def load_env() -> dict:
    """Lit le .env (python-dotenv) et l'exporte vers os.environ.

    L'export est indispensable : les apps (window_config.py, upu/config.py)
    lisent leur géométrie via os.getenv() dans les process enfants. Sans lui,
    un shell parent contenant une valeur OBSOLÈTE (ex: UPU_WINDOW_CLI=0 héritée
    d'un ancien go_ori.ps1) l'emporterait sur le .env — l'app UPU s'ouvrirait
    alors en pleine hauteur malgré la CLI.
    """
    env: dict = {}

    values = dotenv_values(ENV_PATH)
    if not values:
        print(f"[WARN] Fichier .env vide ou introuvable : {ENV_PATH}")
        return env

    for key, caster in LAUNCHER_KEYS.items():
        if key not in values:
            continue
        try:
            env[key] = caster(values[key])
        except Exception:
            env[key] = values[key]

    for key, value in env.items():
        os.environ[key] = str(value)

    return env

