# app_data

Ce dossier contient les donnees persistantes de l'application.

## Fichiers

### app_build.json

Source de verite pour les metadonnees de build utilisees par le code.

Cles attendues:

- version (str)
- latest_check_at (str, format recommande: YYYY-MM-DD HH:MM)
- cache_delay (int > 0, en secondes)

Notes:

- Ce fichier est une reference partagee et peut etre lu/maj par plusieurs composants
    (config applicative, services UI/non-UI, scripts, workflow CI/CD).
- src/upu/config.py le charge pour exposer les constantes de build au code Python.
- Si une cle obligatoire manque ou est invalide,
  l'application leve une erreur au démarrage.
- Dans l'etat actuel du code, latest_check_at est mis a jour apres un check GitHub.

### app_state.json

Stockage runtime mutable (etat applicatif).

Exemples de cles actuelles:

- last_open_release_url_at
- update.last_check_at
- update.latest_version

## Regle de separation

- config.py: constantes applicatives de code (routes, UI, endpoints derives).
- app_build.json: metadonnees de build centralisees.
- app_state.json: etat runtime evolutif.
