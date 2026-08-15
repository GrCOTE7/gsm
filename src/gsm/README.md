# gsm

En travaux → branche declarative

## Flux

### Simplifié

```bash
src/main.py
    ↓
AppBootstrap
    ↓
App
    ↓
MainLayout
    ↓
Router
    ↓
View
    ↓
Components
```

### Flux détaillé (Ordre de l'appel des fichiers)

```bash
uv run flet run
        v
src/main.py
        v
bootstrap/ AppBootstrap
    +--> page.render(App)
        |
        v
    config/ AppConfig - Charge Config
        +--> default home_path pour forcing
        +--> config/ WindowConfig - Configure fenêtre
        +--> initialise Services - À venir
        +--> initialise Session - À venir
        |
        v
    helpers/env.py - get_env, curr_time, nf, dv (debug var)
        |
        v
    config/ AppWindow - Configure ft.Page (title, ...)
    |
    v
App
    +--> routing/Router
        À venir :
            +--> Provider
            +--> Theme
        +--> layouts/ MainLayout
        +--> views/pages/ NotFoundPage
        +--> routing/ PageRoute
            +--> config/ AppConfig (is_index())

            +--> views/pages/ HomePage
            +--> views/pages/ AboutPage
            +--> views/pages/ CounterPage
            +--> views/pages/ TestPage
```

## Structure (Dossiers et fichiers principaux)

```bash
GSM/                             # Dossier racine du projet (Majuscules)
├── .git/                        # Gestion de version
├── .gitignore                   # Fichiers à ignorer par Git
├── .vscode/                     # Configuration de l'éditeur (ex: settings.json)
│   └── settings.json
├── src/
│   ├── main.py                  # Point d'entrée unique (uv run flet run)
│   └── gsm/                     # Votre package principal
│       ├── __init__.py
│       ├── app.py               # Contient la classe App(ft.UserControl) ou similaire
│       ├── bootstrap/
│       │   ├── __init__.py
│       │   └── app_bootstrap.py # Logique d'initialisation (Services, Session...)
│       ├── config/
│       │   ├── __init__.py
│       │   └── app_window.py    # Votre @dataclass AppWindow
│       ├── core/                # Code LOGIQUE uniquement (Zéro interface graphique)
│       │   ├── __init__.py
│       │   ├── database.py      # Exemple : Gestion DB
│       │   └── auth_service.py  # Exemple : Gestion Token / Login
│       ├── layouts/
│       │   ├── __init__.py
│       │   └── main_layout.py   # Structure globale (Sidebar, AppBar)
│       ├── routing/
│       │   ├── __init__.py
│       │   └── router.py        # Gestionnaire de routes / vues
│       ├── views/
│       │   ├── __init__.py
│       │   ├── home_view.py     # Exemple de vue (Page complète)
│       │   └── settings_view.py
│       └── components/
│           ├── __init__.py
│           └── custom_button.py # Composants graphiques réutilisables
├── pyproject.toml               # Configuration des dépendances (géré par uv)
├── README.md                    # Documentation du projet              # Géré par uv
```

## Mémo

### config.py VS settings.py

config.py :

- clés API
- constantes métier
- options de services
- paramètres de scraping
- chemins personnalisés
- règles internes

VS

settings.py :

- configuration de la base de données
- middleware
- applications installées
- routes statiques
- sécurité
- internationalisation
- logs
- templates
- cache
- email
- etc.

### Pour un lancement direct d'un fichier

```bash
pip install -e . 
```
