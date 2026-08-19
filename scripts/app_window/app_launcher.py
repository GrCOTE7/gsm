"""Orchestration du lancement des apps GSM / UPU (modes publics et internes)."""

import os
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path

from cli_spawner import (
    spawn_cli_if_needed,
    place_cli_window,
    _close_stale_cli,
    get_ancestor_pids,
)
from common import (
    MAIN_PY,
    CLI_TOP,
    CLI_WIDTH,
    CLI_HEIGHT,
    SUFFIX_CLI,
    SUFFIX_DETACHED,
    child_arg,
)
from env_config import load_env, window_left, wants_cli
from flet_runner import run_flet, _build_flet_command, _resolve_main_file
from mode_resolver import LaunchAction

# Répertoire temporaire partagé avec go.ps1 et cli_watcher.ps1 (lien entre les
# CLI dédiées du mode ./go gu : fichiers .pid + flag de remplacement).
TEMP_DIR = Path(os.environ.get("TEMP", os.environ.get("TMP", "")))


def launch_app(action: LaunchAction) -> None:
    """Lance toutes les apps demandées par `action`, dans leur contexte."""
    env = load_env()

    if action.mode == "debug":
        debug_dump(action, env)
        return

    _apply_upu_alone(env, action)

    for app in action.apps:
        _launch_single_app(app, action, env)


# ---------------------------------------------------------------------------
# Mode debug (./go debug : affiche, ne lance rien)
# ---------------------------------------------------------------------------


def debug_dump(action: LaunchAction, env: dict) -> None:
    """Affiche tout ce que le launcher ferait, sans rien lancer."""
    print("=== MODE DEBUG ===")
    print("[ACTION] Apps :", action.apps, "-", "[ACTION] Mode :", action.mode)
    print()

    print("[ENV] Variables chargées (Concernant les fenêtres):")
    for key, value in env.items():
        print(f"\t{key} = {value}")
    print()

    print("[WINDOW] Fenêtres qui seraient préparées :")
    for app in action.apps:
        print(f"    - {app}")
    print()

    print("[CLI] CLI dédiée :")
    for app in action.apps:
        flag = "OUI" if wants_cli(app, env) else "NON"
        print(f"    - {app} : {flag}")
    print()

    print("[FLET] Commandes qui seraient exécutées :")
    for app in action.apps:
        cmd = _build_flet_command(_resolve_main_file(app), action.mode)
        print(f"    - {' '.join(cmd)}")
    print()

    print("=== FIN DEBUG ===")


# ---------------------------------------------------------------------------
# Cas particulier : UPU seule (./go u)
# ---------------------------------------------------------------------------


def _apply_upu_alone(env: dict, action: LaunchAction) -> None:
    """./go u (UPU SEULE) : UPU prend la place de GSM.

    En mode normal (./go gu), UPU s'ouvre à UPU_WINDOW_LEFT (à côté de GSM).
    Quand UPU est seule, inutile de laisser vide la place réservée à GSM : la
    position effective devient GSM_WINDOW_LEFT, avec ou sans CLI dédiée.

    Implémentation : le parent pose UPU_ALONE=1 (hérité par la CLI dédiée et
    l'app), puis on force UPU_WINDOW_LEFT := GSM_WINDOW_LEFT dans env +
    os.environ. L'enfant CLI relit le .env (UPU_WINDOW_LEFT=2445) dans son
    propre launch_app : le flag hérité réapplique alors le même forçage
    (idempotent).
    """
    if action.apps == ["upu"] and not action.internal_child:
        os.environ["UPU_ALONE"] = "1"

    if os.environ.get("UPU_ALONE") == "1":
        gsm_left = int(
            env.get("GSM_WINDOW_LEFT", os.environ.get("GSM_WINDOW_LEFT", "1913"))
        )
        env["UPU_WINDOW_LEFT"] = gsm_left
        os.environ["UPU_WINDOW_LEFT"] = str(gsm_left)


# ---------------------------------------------------------------------------
# Dispatch d'une app selon son contexte
# ---------------------------------------------------------------------------


def _launch_single_app(app: str, action: LaunchAction, env: dict) -> None:
    """Lance `app` selon son contexte : CLI dédiée, enfant interne ou simple."""
    if action.internal_child:
        _launch_internal_child(app, action, env)
    elif wants_cli(app, env):
        _launch_cli_parent(app, action, env)
    else:
        _launch_plain(app, action, env)


def _launch_cli_parent(app: str, action: LaunchAction, env: dict) -> None:
    """Process parent demandant une CLI dédiée pour `app`."""
    if _reuse_current_cli(app, action):
        _launch_in_current_cli(app, action, env)
    elif _should_close_stale_cli(app):
        _with_replacing_flag(lambda: _replace_stale_cli(app, env, action.mode))
    else:
        spawn_cli_if_needed(app, env, action.mode)


def _launch_in_current_cli(app: str, action: LaunchAction, env: dict) -> None:
    """Relance depuis une CLI dédiée : on la réutilise, sans nouvelle fenêtre.

    - mono-app → en place (positionnement + Flet bloquant) ;
    - multi-app → enfant détaché (_<app>_child) pour ne pas bloquer la boucle
      qui doit encore spawner l'autre app.
    """
    print(
        f"[CLI] CLI dédiée courante réutilisée pour {app} "
        "(relance depuis la CLI) — aucune nouvelle fenêtre."
    )

    if len(action.apps) == 1:
        # L'app demandée avait peut-être encore une CLI dédiée ailleurs
        # (ex: ./go u relancé depuis la CLI GSM alors qu'une CLI UPU existe
        # encore) → on la remplace par la CLI courante avant de continuer.
        if _should_close_stale_cli(app):
            _with_replacing_flag(lambda: _retarget_current_cli(app))
        _place_current_cli(app, env)
        run_flet(app, env, action.mode)
    else:
        # Multi-app : run_flet est bloquant → on relaie à un enfant détaché
        # qui se charge de cette CLI (positionnement + Flet), et le parent
        # continue pour spawner l'autre app.
        _spawn_app_detached(app, env, action.mode, suffix=SUFFIX_CLI)


def _launch_internal_child(app: str, action: LaunchAction, env: dict) -> None:
    """Enfant : repositionne la CLI courante (sauf si détaché) puis lance Flet.

    Enfant d'une CLI dédiée (_<app>_child) : on repositionne la console sous
    l'app (pixels exacts) puis Flet tourne en bloquant. Enfant détaché en mode
    multi-apps sans CLI (_<app>_nocli) : on n'hérite que de la console, sans
    la repositionner.
    """
    if not action.skip_cli_placement:
        _place_current_cli(app, env)
    run_flet(app, env, action.mode)


def _launch_plain(app: str, action: LaunchAction, env: dict) -> None:
    """Mode sans CLI : Flet se lance et se positionne tout seul.

    run_flet est bloquant (lié à la CLI) : en mode multi-apps, chaque app doit
    donc tourner dans son PROPRE process, sinon la 1ère bloquerait et les
    suivantes ne seraient jamais lancées.
    """
    if len(action.apps) > 1:
        _spawn_app_detached(app, env, action.mode)
    else:
        run_flet(app, env, action.mode)


# ---------------------------------------------------------------------------
# Process détachés et remplacement de CLI dédiée
# ---------------------------------------------------------------------------


def _spawn_app_detached(
    app: str, env: dict, mode: str, suffix: str = SUFFIX_DETACHED
) -> None:
    """Lance une app dans son PROPRE process (non bloquant pour le parent).

    `run_flet` est bloquant (l'app reste liée au cycle de vie de la CLI) : il
    ne peut donc y avoir qu'UN run_flet par process. On relance ce pipeline en
    mode interne "_<app>_<suffix>[_<mode>]" :
    - "nocli" : enfant détaché en mode multi-apps SANS CLI dédiée (./go gu
      sans *_WINDOW_CLI) — n'hérite que de la console, ne la repositionne pas ;
    - "child" : enfant d'une CLI dédiée RÉUTILISÉE (./go gu relancé depuis une
      CLI dédiée) — hérite de la console courante, la repositionne
      (place_cli_window) puis lance Flet.
    """
    subprocess.Popen([sys.executable, str(MAIN_PY), child_arg(app, mode, suffix)])


def _with_replacing_flag(step: Callable[[], None]) -> None:
    """Exécute `step` en posant le flag « remplacement planifié ».

    Le watcher de liaison (cli_watcher.ps1) ne doit PAS interpréter la mort
    d'une CLI pendant un remplacement planifié comme une fermeture de l'autre.
    """
    _set_replacing_flag(True)
    try:
        step()
    finally:
        _set_replacing_flag(False)


def _replace_stale_cli(app: str, env: dict, mode: str) -> None:
    """Remplace l'ancienne CLI dédiée de `app` par une neuve (process parent).

    L'app a peut-être encore une CLI dédiée ailleurs (relance de ./go gu
    depuis une CLI dédiée) : on la ferme, puis on ouvre une console neuve —
    créée à proximité de la bonne position par cli_spawner. C'est elle qui
    relance ce pipeline en mode interne (_gsm_child) et lance Flet. On attend
    que la nouvelle CLI écrive son .pid, puis on relâche le flag (sinon le
    watcher croirait à une fermeture).
    """
    old_pid = _read_pid(app)
    _close_stale_cli(app)
    spawn_cli_if_needed(app, env, mode)
    _wait_for_new_cli_pid(app, old_pid)


def _retarget_current_cli(app: str) -> None:
    """La CLI courante change d'app : on réécrit le .pid et on ferme l'ancienne.

    Cas : CLI GSM relancée en ./go u alors qu'une CLI UPU existe encore. Le
    .pid de la CLI courante est réécrit sous `app` (détection future), puis
    l'ancienne CLI de `app` est fermée et on laisse le watcher constater la
    rupture de lien.
    """
    current = _current_cli_app()
    if current:
        old_pid = _read_pid(current)
        _cli_pid_file(current).unlink(missing_ok=True)
        if old_pid is not None:
            _cli_pid_file(app).write_text(str(old_pid), encoding="ascii")
    _close_stale_cli(app)
    time.sleep(2.5)


def _place_current_cli(app: str, env: dict) -> None:
    """Repositionne la fenêtre du terminal courant sous la fenêtre de l'app."""
    place_cli_window(
        left=window_left(app, env),
        top=CLI_TOP,
        width=CLI_WIDTH,
        height=CLI_HEIGHT,
    )


# ---------------------------------------------------------------------------
# Détection de la CLI dédiée courante (fichiers .pid dans %TEMP%)
# ---------------------------------------------------------------------------


def _reuse_current_cli(app: str, action: LaunchAction) -> bool:
    """Vrai si la CLI dédiée COURANTE doit être réutilisée pour `app`.

    - mono-app → la CLI courante est toujours réutilisée ;
    - multi-app (./go gu) → seule l'app que la CLI courante héberge déjà est
      réutilisée — l'autre est spawnée.
    """
    current = _current_cli_app()
    if current is None:
        return False
    if len(action.apps) == 1:
        return True
    return current == app


def _should_close_stale_cli(app: str) -> bool:
    """Vrai s'il faut remplacer une ancienne CLI dédiée de `app`.

    On est dans une CLI dédiée et l'app cible n'est pas la CLI courante.
    L'existence réelle de la CLI de `app` est vérifiée par _close_stale_cli
    (filtre Get-CimInstance sur 'go.ps1 _<app>_child').
    """
    current = _current_cli_app()
    if current is None:
        return False
    return current != app


def _current_cli_app() -> str | None:
    r"""App de la CLI dédiée courante ('gsm'/'upu'), ou None hors CLI dédiée.

    go.ps1 écrit le PID de la console dans %TEMP%\gsm_cli_<app>.pid en mode
    _<app>_child : on compare la chaîne des ancêtres du process courant (le
    pwsh de la console, éventuellement via uv) à ces fichiers. Fiable même si
    l'environnement n'est pas hérité (wt.exe relaie au serveur Windows
    Terminal, dont l'environnement est figé).
    """
    ancestors = get_ancestor_pids(os.getpid())
    for app in ("gsm", "upu"):
        pid = _read_pid(app)
        if pid is not None and pid in ancestors:
            return app
    return None


def _cli_pid_file(app: str) -> Path:
    """Fichier .pid écrit par go.ps1 pour une CLI dédiée (mode _<app>_child)."""
    return TEMP_DIR / f"gsm_cli_{app.lower()}.pid"


def _read_pid(app: str) -> int | None:
    """PID de la CLI dédiée de `app`, ou None si absent/invalide."""
    pid_file = _cli_pid_file(app)
    if not pid_file.exists():
        return None
    try:
        return int(pid_file.read_text(encoding="ascii").strip())
    except ValueError:
        return None


def _set_replacing_flag(on: bool) -> None:
    """Pose ou retire le flag « remplacement planifié » partagé avec le watcher."""
    flag = TEMP_DIR / "gsm_cli_replacing"
    if on:
        flag.write_text("1", encoding="ascii")
    else:
        flag.unlink(missing_ok=True)


def _wait_for_new_cli_pid(app: str, old_pid: int | None, timeout: float = 12.0) -> None:
    """Attend que la NOUVELLE CLI de `app` ait écrit son .pid (≠ ancien PID)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        current = _read_pid(app)
        if current is not None and current != old_pid:
            return
        time.sleep(0.3)



