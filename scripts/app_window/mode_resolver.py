"""Résolution du mode de lancement demandé à ./go.

Traduit l'option CLI ('' / 'w' / 'u' / 'gu' / 'debug') ainsi que les modes
internes "_<app>_<child|nocli>[_<mode>]" en une LaunchAction consommable par
app_launcher.
"""

from dataclasses import dataclass, field

APP_NAMES = ("gsm", "upu")
DEFAULT_APP = "gsm"
DEFAULT_MODE = "app"


@dataclass(frozen=True)
class LaunchAction:
    """Ce que le launcher doit faire pour une invocation de ./go."""

    apps: list[str] = field(default_factory=lambda: [DEFAULT_APP])
    mode: str = DEFAULT_MODE
    internal_child: bool = False
    skip_cli_placement: bool = False


# Options publiques de ./go -> action correspondante.
PUBLIC_MODES: dict[str, LaunchAction] = {
    "": LaunchAction([DEFAULT_APP], DEFAULT_MODE),
    "w": LaunchAction([DEFAULT_APP], "web"),
    "u": LaunchAction(["upu"], DEFAULT_MODE),
    "gu": LaunchAction([DEFAULT_APP, "upu"], DEFAULT_MODE),
    "debug": LaunchAction([DEFAULT_APP], "debug"),
}


def resolve_mode(mode: str) -> LaunchAction:
    """Convertit l'option CLI en action de lancement.

    Modes publics : '' (GSM app), 'w' (GSM web), 'u' (UPU seule),
    'gu' (GSM + UPU), 'debug' (affichage sans lancement).
    Modes internes : "_<app>_<child|nocli>[_<mode>]" (ex : _gsm_child_web).
    Toute option inconnue retombe sur le comportement par défaut (GSM, APP).
    """
    normalized = mode.lower().strip()

    if normalized.startswith("_"):
        return _resolve_internal(normalized)

    return PUBLIC_MODES.get(normalized, PUBLIC_MODES[""])


def _resolve_internal(raw_mode: str) -> LaunchAction:
    """Traduit un mode interne enfant ("_<app>_<suffix>[_<mode>]").

    Ces modes sont générés par cli_spawner/app_launcher pour relancer ce
    pipeline dans un process enfant sans rouvrir de CLI (sinon récursion) :
    - suffix "child" : CLI dédiée RÉUTILISÉE — hérite de la console courante
      et la repositionne (place_cli_window) ;
    - suffix "nocli" : enfant détaché en mode multi-apps SANS CLI dédiée
      (./go gu sans *_WINDOW_CLI) — n'hérite que de la console, ne la
      repositionne pas.
    """
    parts = raw_mode[1:].split("_")
    app = parts[0] if parts and parts[0] in APP_NAMES else DEFAULT_APP
    suffix = parts[1] if len(parts) > 1 else "child"
    child_mode = parts[2] if len(parts) > 2 and parts[2] in ("app", "web") else DEFAULT_MODE

    return LaunchAction(
        apps=[app],
        mode=child_mode,
        internal_child=True,
        skip_cli_placement=suffix != "child",
    )
