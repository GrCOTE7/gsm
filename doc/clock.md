# Clock page

* [ ] Avec Approche Déclarative

## Structure

```bash
app/
├── main.py                 # point d'entrée, assemble tout
├── state/
│   ├── clock.py            # état courant de l'heure
│   └── alarm.py            # état de l'alarme (armée, sonne, snooze...)
├── logic/
│   ├── alarm_engine.py     # règles : quand déclencher, snooze, stop
│   └── scheduler.py        # boucle/tic, déclenche les events
├── ui/
│   ├── clock_view.py       # affichage horloge
│   ├── alarm_view.py       # réglage alarme
│   └── ringing_view.py     # écran quand ça sonne
└── events.py               # bus d'événements simple (pub/sub)
```

## Découpage

* state/ → porte l'état pur, sans logique. Ici, une classe par état a du sens (Clock, Alarm), parce qu'il y a un vrai objet à manipuler.

* logic/ → fonctions ou petites classes qui appliquent les règles. Pas besoin d'une classe par règle. Souvent une classe AlarmEngine suffit, avec des méthodes (should_ring(), snooze(), dismiss()).

* ui/ → un module par vue, pas une classe par vue nécessairement. En Flet, tu peux très bien avoir des fonctions qui retournent des ft.Column(...).

* events.py → un petit bus d'événements (pub/sub) qui découple l'UI de la logique. C'est le seul vrai pattern que j'ajouterais, parce que c'est exactement ce qui manque dans un prototype impératif.
* 
### 🧠 Ce qui est déclaratif dans ce découpage

* Le state/
Décrire ce qui est (l'heure, l'alarme armée, snooze actif) sans dire comment on y arrive.
→ C'est déclaratif au sens fort : on décrit un état, pas une procédure.

Le events.py (bus pub/sub)
On ne dit pas « quand X se passe, appelle Y ».
On dit « Y écoute X ».
→ Inversion du contrôle : c'est l'abonné qui décide, pas l'émetteur. Très déclaratif dans l'esprit.

L'ui/ en Flet
Flet est déjà déclaratif par nature : tu décris un arbre de widgets (ft.Column([...])), et le framework se débrouille pour le rendre et le mettre à jour.
→ C'est pour ça que Flet est intéressant ici : il pousse naturellement vers le déclaratif côté UI.

⚙️ Ce qui reste impératif (et c'est normal)
logic/alarm_engine.py : les règles « si l'heure == alarme → sonner », c'est de l'impératif — un enchaînement de conditions et d'actions.

scheduler.py : la boucle de tic, le déclenchement périodique — impératif par nature.

Et c'est très bien comme ça : le déclaratif pur pour un réveil serait artificiel. Un réveil fait des choses dans le temps. Il y a un côté événementiel irréductible.

### .🎯 Règle simple

| Situation                                    | Solution                                       |
| -------------------------------------------- | ---------------------------------------------- |
| Il y a un état à porter (heure, alarme)      | Classe                                         |
| Il y a une règle métier (déclencher, snooze) | Fonction ou méthode dans une classe de service |
| Il y a un affichage (vue Flet)               | Module + fonction qui retourne un widget       |
| Il y a une communication entre composants    | Bus d'événements                               |

### .🎯 Ce que ton intuition capte vraiment

Ta structure sépare :

| Couche      | Paradigme dominant                          |
| ----------- | ------------------------------------------- |
| `state/`    | Déclaratif (description d'état)             |
| `events.py` | Déclaratif (pub/sub, inversion de contrôle) |
| `ui/`       | Déclaratif (Flet, arbre de widgets)         |
| `logic/`    | Impératif (règles, décisions)               |

→ Le déclaratif domine 3 couches sur 4. L'impératif est confiné dans la logique métier, là où il est légitime.

💡 Le vrai bénéfice
Ce n'est pas juste « c'est joli ». C'est que :

L'UI ne connaît pas la logique → elle réagit à des états et des événements.

La logique ne connaît pas l'UI → elle publie des événements, sans savoir qui écoute.

L'état est central et unique → une seule source de vérité, comme dans les architectures déclaratives modernes (Redux, Elm, React + hooks, etc.).

C'est exactement le passage d'un prototype impératif Flet à quelque chose qui scale — et c'est précisément ce que Will évoque quand il dit « separate more of that logic into services and more declarative components ».
