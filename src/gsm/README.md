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

`views/` n'est plus un dossier plat : il est découpé en sous-dossiers
spécialisés — `pages/` (1 fichier = 1 route), `partials/` (fragments
réutilisables - header, footer, etc.), `templates/` (gabarits).

```bash
GSM/                              # Dossier racine du projet (Majuscules)
├── .git/                         # Gestion de version
├── .gitignore                    # Fichiers à ignorer par Git
├── .vscode/                      # Configuration de l'éditeur (ex: settings.json)
│   └── settings.json
├── doc/                          # Documentation projet (Git, VSCode, ...)
├── scripts/                      # Scripts utilitaires (PowerShell / Python)
├── tests/                        # Tests pytest
├── src/
│   ├── main.py                   # Point d'entrée unique (uv run flet run)
│   ├── assets/                   # Ressources (icon.png, ...)
│   └── gsm/                      # Votre package principal
│       ├── __init__.py
│       ├── app.py                # App : composant racine (délègue au routeur)
│       ├── config_uuu.py         # Ancien code conservé (archive, non utilisé)
│       ├── bootstrap/
│       │   ├── __init__.py
│       │   └── app_bootstrap.py  # AppBootstrap : amorçage session + page.render(App.view)
│       ├── config/
│       │   ├── __init__.py
│       │   ├── app_config.py     # AppConfig + singleton `config` (home_path, thème)
│       │   ├── window_config.py  # WindowConfig : taille / position de la fenêtre
│       │   ├── app_window.py     # AppWindow : titre de l'onglet (préfixe "L_" en dev)
│       │   └── app_env.py        # AppEnv : détection environnement / plateforme
│       ├── core/            # Code LOGIQUE uniquement (Zéro interface graphique)
│       │   ├── session.py   # À venir (vide)
│       │   ├── settings.py  # À venir (vide)
│       │   └── theme.py     # À venir (vide)
│       ├── components/                    # Composants graphiques réutilisables
│       │   ├── diagnostic
│       │   │   ├── __init__.py
│       │   │   ├── diagnostic_block.py     # ← Card unique qui compose les 3 sections
│       │   │   └── sections/
│       │   │       ├── __init__.py
│       │   │       ├── versions_section.py # OS, Py, Flet
│       │   │       ├── system_section.py   # ← futur (stub)
│       │   │       └── network_section.py  # ← futur (stub)
│       │   └── autre.py                    # (futur)
│       ├── layouts/
│       │   └── main_layout.py    # MainLayout : Pagelet persistant + use_route_outlet
│       ├── routing/
│       │   ├── routes_registry.py # PageRoute + PAGES : SEULE source de vérité des routes
│       │   └── router.py         # AppRouter : construit l'arbre ft.Route
│       ├── states/               # États observables partagés
│       │   └── counter_state.py  # CounterState (@ft.observable) du compteur
│       ├── helpers/              # Fonctions utilitaires
│       │   ├── env.py            # get_env, is_dev_env, curr_time, nf, dv, dvd
│       │   ├── diagnostic.py     # collect_versions, collect_system, collect_network
│       │   ├── refs.py           # gh_url, gh_link, year_day, aff
│       │   ├── separators.py     # sepa, sepa_outlined
│       │   └── quick_test.py     # Bac à sable / essais ponctuels
│       ├── services/             # Accès données / monde extérieur
│       │   └── release_service.py # Ouverture du lien de release (throttle 1×/heure)
│       ├── guests/               # Contenus "invités" (registre)
│       │   ├── __init__.py       # REGISTRY + register()
│       │   ├── g260530_nom.py
│       │   ├── g260602_mln_913.py
│       │   ├── g260629_mln.py
│       │   ├── g260799_.py
│       │   └── g999999_matrice.py
│       ├── views/                # Tout ce qui s'affiche
│       │   ├── pages/            # Pages complètes (1 fichier = 1 route)
│       │   │   ├── home.py       # HomePage  → /
│       │   │   ├── about.py      # AboutPage → /about
│       │   │   ├── counter.py    # CounterPage → /counter
│       │   │   ├── test.py       # TestPage  → /test
│       │   │   └── not_found.py  # NotFoundPage (404, catch-all, hors NavBar)
│       │   ├── partials/         # Fragments contexttuels (route aware)
│       │   │   ├── __init__.py
│       │   │   ├── footer.py               # Pieds de page
│       │   │   ├── header.py               # Header
│       │   │   ├── nav_bar.py              # NavBar : AppBar + NavigationDrawer (lit PAGES)
│       │   │   ├── release_update_card.py  # build_release_update_card()
│       │   │   ├── test_guests_src.py      # guest_source()
│       │   └── templates/        # Gabarits de mise en page
│       │       └── default.py    # named_view() : titre + corps + extra + bottom
│       └── z_doc/
│           └── DOC_DECLARATIVE.md # Notes d'architecture (Flet déclaratif 0.85)
├── pyproject.toml                 # Configuration des dépendances (géré par uv)
└── README.md                      # Documentation du projet
```

À retenir :

- **Routage** : pour ajouter une page, créez sa classe dans
  `views/pages/`, puis enregistrez-la dans `PAGES`
  (`routing/routes_registry.py`). Ni le routeur ni la NavBar ne sont à
  modifier.
- **Component** : Code indépendant de la page
- **Emplacement** : une page complète va dans `views/pages/`, un fragment
  réutilisable — partials (header, carte, footer...) dans `views/partials/`.
- **`__init__.py`** : uniquement là où il est utile (`bootstrap/`,
  `config/`, `guests/`, `views/partials/`). Les autres dossiers sont des
  *namespace packages* implicites (PEP 420) et s'importent normalement,
  ex. `from gsm.views.pages.home import HomePage`.
- `core/` ne contient aucune interface graphique (session, settings,
  thème : à venir) ; les fichiers listés « À venir (vide) » sont des
  emplacements réservés.

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
