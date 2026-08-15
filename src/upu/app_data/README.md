# app_data

Ce dossier contient les donnees persistantes de l'application.

## Fichiers

### app_build.json

Source de verite pour les métadonnées de build locales utilisées par le code.

Clés attendues:

- version (str)
- cache_delay (int > 0, en secondes)

Notes:

- Ce fichier décrit ce qui est embarque localement avec l'application.
- Il ne doit pas contenir le cache de la derniere release GitHub connue.
- src/gsm/services/state_repository.py le charge pour exposer les métadonnées
    de build au reste du code.
- Si une cle obligatoire manque ou est invalide,
  l'application lève une erreur au démarrage.

### app_state.json

Stockage runtime mutable (État applicatif).

Exemples de clés actuelles:

- last_open_release_url_at
- latest_check_at
- update.latest_release_info

Notes:

- Ce fichier contient les informations apprises ou mises en cache a l'execution.
- Le cache de release GitHub y est stocke séparément de la version locale installée.
- src/gsm/services/state_repository.py centralise les accès lecture/écriture.

## Règle de separation

- config.py: constantes applicatives de code (routes, UI, endpoints derives).
- app_build.json: métadonnées de build locales centralisées.
- app_state.json: État runtime évolutif.
- state_repository.py: couche d'accès unique pour app_build.json et app_state.json.
