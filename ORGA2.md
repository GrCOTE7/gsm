# Organigramme (version présentation)

Ce document présente le processus de mise à jour en 2 blocs visuels:

- avant le clic sur « Mettre à jour »
- après le clic sur « Mettre à jour »

## Bloc 1 - Avant clic (détection et popup)

```mermaid
flowchart TD
    A["Démarrage de l'app"] --> B["src/main.py<br/>ft.run(create_app)"]
    B --> C["src/upu/controllers/app_controller.py<br/>create_app -> AppController"]
    C --> D["_render_route<br/>lance _maybe_prompt_for_update (1 seule fois)"]

    D --> E{"is_update_available ?"}
    E -- "Non" --> F["Pas de popup<br/>l'application continue"]
    E -- "Oui" --> G["get_latest_release_info"]
    G --> H["_show_update_dialog"]
    H --> I["Popup AlertDialog<br/>Plus tard / Mettre à jour"]
```

## Bloc 2 - Après clic sur « Mettre à jour »

```mermaid
flowchart TD
    A["Clic bouton Mettre à jour"] --> B["_install_update(release_url)<br/>src/upu/controllers/app_controller.py"]
    B --> C["Ferme le popup"]
    C --> D["SnackBar: tentative d'ouverture"]
    D --> E["open_release_url(page, release_url, force=True)"]

    E --> F{"URL ouverte ?"}
    F -- "Non" --> G["SnackBar d'échec"]
    F -- "Oui" --> H["SnackBar d'information (log)"]

    E --> I["src/upu/services/release_service.py
    launch_url -> page.open(ft.Url) -> webbrowser.open"]
    I --> J["Log: src/upu/app_data/update_flow.log"]
```

## Références fichiers

- src/main.py
- src/upu/controllers/app_controller.py
- src/upu/config.py
- src/upu/services/release_service.py
- src/upu/app_data/update_flow.log

## Lecture rapide

1. L'application démarre et vérifie s'il existe une version plus récente sur GitHub.
2. Si oui, elle affiche un popup de confirmation
   avec « Plus tard » et « Mettre à jour ».
3. Au clic sur « Mettre à jour », elle tente d'ouvrir le lien de release APK.
4. Elle affiche ensuite un retour utilisateur (succès ou échec)
   et journalise la tentative.
