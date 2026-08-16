import os

ENV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", ".env")

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
    env = {}

    if not os.path.exists(ENV_PATH):
        print(f"[WARN] Fichier .env introuvable : {ENV_PATH}")
        return env

    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.split("#")[0].strip()

            if key in LAUNCHER_KEYS:
                caster = LAUNCHER_KEYS[key]
                try:
                    env[key] = caster(value)
                except:
                    env[key] = value

    # EXPORT : les valeurs du .env doivent aussi être visibles des process
    # enfants (CLI dédiée, process Flet...). Les apps (window_config.py,
    # upu/config.py) lisent en effet leur géométrie via os.getenv().
    # Sans cet export, un shell parent contenant une valeur OBSOLÈTE (ex:
    # UPU_WINDOW_CLI=0 héritée d'un ancien go_ori.ps1) l'emporterait sur le
    # .env — l'app UPU s'ouvrirait alors en pleine hauteur malgré la CLI.
    for key, value in env.items():
        os.environ[key] = str(value)

    return env
