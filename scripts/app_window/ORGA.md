# ./go

## Récapitulatif

| Fonction                                         | Fichier                               |
| ------------------------------------------------ | ------------------------------------- |
| Script d'entrée bash                             | `go` (racine)                         |
| Lanceur PowerShell                               | `go.ps1` (racine)                     |
| Lecture des args + dispatch                      | `scripts/app_window/main.py`          |
| Résolution du mode (dont `_gsm_child`)           | `scripts/app_window/mode_resolver.py` |
| Orchestration (`launch_app`, `place_cli_window`) | `scripts/app_window/app_launcher.py`  |
| Ouverture de la CLI wt + chemins pwsh/wt         | `scripts/app_window/cli_spawner.py`   |
| Commande Flet (`sys.executable -m flet.cli`)     | `scripts/app_window/flet_runner.py`   |
| Lecture du `.env`                                | `scripts/app_window/env_config.py`    |
| Géométrie/positionnement de la fenêtre de l'app  | `src/gsm/config/window_config.py`     |

## Organigramme

```mermaid
flowchart TD
    A["'./go' (bash)<br/>uv run python scripts/app_window/main.py<br/>[go]"] --> B["main.py : get_mode() = ''<br/>[scripts/app_window/main.py]"]
    B --> C["resolve_mode('') : {apps:[gsm], mode:app}<br/>[scripts/app_window/mode_resolver.py]"]
    C --> D["launch_app(action)<br/>lit .env (GSM_WINDOW_CLI, GSM_WINDOW_LEFT)<br/>[scripts/app_window/app_launcher.py]<br/>[scripts/app_window/env_config.py]"]

    D --> E{"GSM_WINDOW_CLI = 1 ?<br/>[.env]"}

    E -- "0 : pas de CLI dediee" --> F["run_flet(gsm)<br/>python -m flet.cli run src/main_gsm.py -r<br/>[scripts/app_window/flet_runner.py]"]
    F --> G["Flet se positionne seul (window_config)<br/>1913,0 x 540x779<br/>[src/gsm/config/window_config.py]"]

    E -- "1 : CLI dediee" --> H["spawn_cli_if_needed() -> _spawn_cli_windows()<br/>[scripts/app_window/cli_spawner.py]"]
    H --> I["wt.exe -w new --pos 1913,780 --size 60,12 -d C:/gsm<br/>pwsh -NoExit -File go.ps1 _gsm_child<br/>[go.ps1]"]

    I --> J["[ENFANT] main.py _gsm_child<br/>resolve_mode -> {gsm, app, internal_child}<br/>[main.py + mode_resolver.py]"]
    J --> K["place_cli_window(1913, 779, 540, 300)<br/>cadre WindowsTerminal repositionne (pixels exacts)<br/>[scripts/app_window/app_launcher.py]"]
    K --> L["run_flet(gsm)<br/>python -m flet.cli run src/main_gsm.py -r<br/>[scripts/app_window/flet_runner.py]"]
    L --> M["App Flet (1913,0 x 540x779)<br/>+ CLI dediee collee dessous (779 x 540x300)<br/>[src/main_gsm.py + app_launcher.py]"]

    style E fill:#fff3bf,stroke:#e6b800
    style K fill:#d3f9d8,stroke:#37b24d
```

## Cycle de vie (depuis le fix "l'app ne survit plus à sa CLI")

`run_flet()` (flet_runner.py) est **bloquant** : le launcher reste vivant tant que
l'app Flet tourne, et **la fermeture de la CLI ferme l'app** :

- **CTRL+C** → `KeyboardInterrupt` → `finally` → `taskkill /PID <flet> /T /F`
  (toute l'arborescence `uv → python → flet → app` est tuée).
- **Croix / logoff / shutdown** (Windows) → handler de console
  (`_watchdog_console_close`) qui tue l'arborescence avant la terminaison.
- **Linux** → SIGINT / SIGHUP atteignent naturellement tout le groupe de process.

Conséquence : en mode multi-apps **sans CLI dédiée** (`./go gu`, `_CLI=0`), chaque
app est lancée dans son **propre process** (`_spawn_app_detached`, mode interne
`_gsm_nocli`), sinon un `run_flet` bloquant empêcherait le lancement des suivantes.

