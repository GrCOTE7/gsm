# GSM — squelette Flet déclaratif (0.85.3)

## Lancer le projet

```bash
pip install -r requirements.txt
cd src
python main.py
# ou, pour le hot-reload : flet run main.py -d -r
```

## Ce qui a été corrigé

Le code d'origine plantait pour plusieurs raisons, toutes liées au fait
qu'il mélangeait l'**ancien** modèle impératif de Flet (`page.views`,
`page.on_route_change`, `page.go()`) avec le **nouveau** modèle déclaratif
(`@ft.component`, `ft.use_state`) — les deux ne sont pas interopérables
de cette façon :

1. **`router.py`** appelait `ViewClass()` puis enveloppait le résultat
   dans un `ft.Container` classique, alors que `Counter()` retourne un
   composant décoré `@ft.component` : celui-ci doit être rendu par le
   moteur déclaratif (via `page.render`/`page.render_views`), pas
   instancié et manipulé à la main comme un control impératif.
2. **`setup.py`** appelait à la fois l'ancien routage (`page.go("/")`,
   `route(page)` avec `on_route_change`) et le nouveau (`page.render(...)`)
   sur le même `page` — les deux systèmes se marchaient dessus.
3. **`app.py`** lisait `self.page.views[-1]`, qui n'est jamais rempli
   puisque rien n'utilise plus l'API `page.views` impérative une fois
   passé au rendu déclaratif.

Depuis **Flet 0.85**, il existe un routeur déclaratif natif,
`ft.Router` / `ft.Route`, calqué sur React Router (routes imbriquées,
layouts avec `outlet`, segments dynamiques, etc.). C'est lui qui remplace
tout le routage manuel ci-dessus — voir `gsm/core/router.py`.

## Pourquoi des `staticmethod` plutôt que des méthodes normales ?

Les hooks (`ft.use_state`, `ft.use_effect`, `ft.use_ref`...) ne
fonctionnent que sur des fonctions "nues" appelées à chaque rendu — au
même titre que les Hooks React, qui ne fonctionnent pas non plus dans une
classe. Décorer une méthode liée (`self.view`) avec `@ft.component`
casserait le suivi d'état interne du framework.

Le compromis retenu ici pour rester le plus proche possible de la POO :
chaque page/layout est une **classe qui sert de namespace**, et le
composant réel est une `@staticmethod` décorée par `@ft.component` :

```python
class CounterPage:
    @staticmethod
    @ft.component
    def view() -> ft.Control:
        count, set_count = ft.use_state(0)
        ...
```

Résultat : `CounterPage.view` s'utilise exactement comme une fonction de
composant classique (`ft.Route(component=CounterPage.view)`,
`page.render(App.view)`, etc.), tout en gardant vos pages regroupées et
organisées en classes.

## Pour aller plus loin : état partagé/OOP avec `@ft.observable`

Pour un état plus complexe que `use_state` (partagé entre plusieurs
composants, avec des méthodes métier), Flet propose `@ft.observable` :
une classe "normale" (dataclass ou non) devient réactive, un peu comme un
store MobX/Zustand :

```python
from dataclasses import dataclass
import flet as ft

@ft.observable
@dataclass
class CounterState:
    value: int = 0

    def increment(self) -> None:
        self.value += 1

    def decrement(self) -> None:
        self.value -= 1
```

C'est le pattern à privilégier si vous voulez pousser la logique métier
dans de vraies classes avec des méthodes, plutôt que dans des closures
`handle_xxx` locales au composant.

## Accès à `page` sans le faire remonter partout

Notez qu'aucun composant ne reçoit plus `page` en paramètre de
constructeur : `ft.context.page` donne accès à la page courante depuis
n'importe quel composant (ex. `NotFoundPage`), comme un `useContext` en
React. C'est ce qui a permis de retirer `self.page` de `App` et
`MainLayout`.

## Structure

```
src/
├── main.py
└── gsm/
    ├── app.py                  # Composant racine
    ├── bootstrap/
    │   └── setup.py            # Point d'entrée de session (ft.run)
    ├── core/
    │   ├── config.py           # Réglages (fenêtre, thème...)
    │   └── router.py           # Table de routes (ft.Router / ft.Route)
    ├── layouts/
    │   └── main_layout.py      # Layout persistant + use_route_outlet
    └── views/pages/
        ├── counter.py
        └── p404.py
```
