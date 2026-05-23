# app_data

Ce dossier contient les donnees persistantes de l'application.

## Fichiers

### app_build.json

Source de verite pour les metadonnees de build locales utilisees par le code.

Cles attendues:

- version (str)
- cache_delay (int > 0, en secondes)

Notes:

- Ce fichier decrit ce qui est embarque localement avec l'application.
- Il ne doit pas contenir le cache de la derniere release GitHub connue.
- src/upu/services/state_repository.py le charge pour exposer les metadonnees
    de build au reste du code.
- Si une cle obligatoire manque ou est invalide,
  l'application leve une erreur au démarrage.

### app_state.json

Stockage runtime mutable (etat applicatif).

Exemples de cles actuelles:

- last_open_release_url_at
- latest_check_at
- update.latest_release_info

Notes:

- Ce fichier contient les informations apprises ou mises en cache a l'execution.
- Le cache de release GitHub y est stocke separement de la version locale installee.
- src/upu/services/state_repository.py centralise les acces lecture/ecriture.

## Regle de separation

- config.py: constantes applicatives de code (routes, UI, endpoints derives).
- app_build.json: metadonnees de build locales centralisees.
- app_state.json: etat runtime evolutif.
- state_repository.py: couche d'acces unique pour app_build.json et app_state.json.
