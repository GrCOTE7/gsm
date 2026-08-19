"""Constantes et helpers partagés du launcher (scripts/app_window).

Regroupe ce qui est partagé entre cli_spawner.py, app_launcher.py,
flet_runner.py, env_config.py et demo_configs.py : chemins du dépôt,
géométrie de la CLI dédiée et construction de l'argument interne enfant.
"""

from pathlib import Path

# Racine du dépôt (app_window -> scripts -> gsm).
ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / ".env"
MAIN_PY = ROOT / "scripts" / "app_window" / "main.py"
GO_PS1 = ROOT / "go.ps1"

# Fenêtre CLI dédiée, collée sous l'app (pixels exacts).
CLI_WIDTH = 540
CLI_HEIGHT = 300
CLI_TOP = 779

# Suffixes des modes internes enfant (voir mode_resolver._resolve_internal).
SUFFIX_CLI = "child"
SUFFIX_DETACHED = "nocli"


def child_arg(app: str, mode: str, suffix: str) -> str:
    """Construit l'argument interne enfant : "_<app>_<suffix>[_<mode>]".

    suffix = "child" (CLI dédiée) ou "nocli" (détaché, multi-apps sans CLI).
    Exemples : _gsm_child, _gsm_child_web, _upu_nocli.
    """
    arg = f"_{app.lower()}_{suffix}"
    if mode and mode != "app":
        arg += f"_{mode}"
    return arg
