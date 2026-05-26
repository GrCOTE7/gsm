# GIT

## ← 3. [0103_GIT_USE](./0103_GIT_USE.md)

## 4. 🏗️ On attaque **le dev** ?

Juste pour te rassurer : Bon, jusqu'à maintenant, beaucoup de lecture pour bien comprendre et tout assimiler... Mais crois-moi: Si demain, tu dois tout recommencer, tu mettras max 2 minutes même si t'es pas doué 😉 ! Et ce principe sera toujours vrai 👍 - Bref, tu ne t'en aperçois p't'être même pas, mais tu d'viens bon 👌 ! Alors, courage pour la suite !

### .🎯 L’idée principale

Toujours oeuvrer dans une branche dédiée avant de commencer un développement spécifique. Cela garde un historique propre au moins sur la branche main, facilite les revues de code et évite donc de casser la branche principale qui doit toujours rester stable, au cas où... Et insdipensable pour un dev collaboratif.

    Pour info, une branche est comme une sorte d'autre copie intégrale du projet ! À ceci prêt que l'algorithme de GitHub (ou autre fournisseur) ne duplique pas vraiment tous les fichiers, mais garde 'simplement' en mémoire toutes les modifications, bref, quelques fichiers texte de quelques octets...
    
    Donc, très léger, mais surtout complètement transparent pour nous : Ne pas hésiter à en abuuser !

### 🧩Donc, étape 1 — Créer une branche de travail

Tu peux nommer ta branche comme tu veux, mais voici la [norme idéalement](https://codeheroes.fr/blog/git-comment-nommer-ses-branches-et-ses-commits) :

* tout en minuscule, aucun accent
* pas d’espaces, utiliser des tirets - ou /
* refléter le type de travail (feature, fix, doc…) et le sujet du dev

Exemples de conventions :

* feature/new-service
* fix/bug-update-btn
* doc/upgrade-readme

Cela rend l’historique compréhensible et navigable pour toute l’équipe.

### → 🛠️ 2ème Commande Git (Car déjà vu 'le' *clone*...)

En CLI, elle créée la branche 'upgrade/01_git-dev' et te pose dessus :

```bash
git branch upgrade/01_git-dev
git checkout upgrade/01_git-dev
    # OU - ménémonique, mais + court :
git checkout -b upgrade/01_git-dev
    # ET + moderne :
git switch -c upgrade/01_git-dev
```

Pour faire si besoin le point et avoir la liste des branches existantes :

```bash
git branch
```
    
Affiche les branches locales, avec * sur celle où tu es.

(Si " :" au lieu de ton invite habituelle :, c'est qu'on est en mode édition. Tape 'ESC4, 'x' ou ':q' pour *e**X**it* ou ***Q**uit* (sortir de cet éditeur [**vi** ou **vim**](https://blog.stephane-robert.info/_astro/vi_demo.9jUPpoF3_Z27rg4g.webp)))

Pour passer sur une autre branche (Par exemple, revenir sur la branche main) :

```bash
git checkout main
    # ET + moderne :
git switch main
    # À noter
git switch - # Retour sur la branche précédente
```

Voici qqes commandes utiles liées aux branches

```bash
git branch ma-branche                    # créée la branche mais sans passer dessus

git branch -d ma-branche                 # détruit la branche
    # + moderne :
git branch --delete ma-branche

git branch -m ancien-nom nouveau-nom     # renomme la branche
    # + moderne :
git branch --move ancien-nom nouveau-nom

git branch -a                        # voir les branches distantes (- a = all)
    # OU :
git branch --all

git checkout HEAD -- fichier.txt
    # + moderne :
git restore fichier.txt
```

### 👉 Même si vous découvrirez bientôt des outils qui rendent intuitives et ludiques ces commandes car applicables 'à coups de souris', il est toujours bon et parfois salvateur de connaître les commandes de base en console.

### 🚧 T.P. - Exercice


Pour comprendre l'importance et la magie du git, voyons un exemple exagéré extrême :
Imaginons que fatigués, tu effaces par erreur tout un dossier important...
Sans le git, cela serait assurément catastrophique, on ne sauvegarde pas toutes les 2 minutes !!!

Donc, passe sur une nouvelle branche

```bash
git checkout -b action_debile
```

Efface tout un dossier/ par accident
→ git checkout -b uuu → efface tout un / 
git restore chemin/du/dossier

* [ ] To be continued... 🚧

Test push depuis codespace

    Exemples:
    
        feature/ma-nouvelle-fonctionnalite

        fix/bug-du-bouton

        doc/amelioration-readme

    → Cela permet de garder l’historique propre et compréhensible.
    
    ```bash
git branch amelioration-01_git
```

    Mais du coup, là, t'es 'chez toi', c'est hyper cool ! tu y dev ce que tu veux, cela ne peut jamais rien casser d'important, et tu te plantes ? Bravo, c'est que tu as poussé tes limites :-) ! Et si tu les as trop dépassées... Pas grave: Revient sur la branche main ! Rien n'est jamais perdu ! Rien qagné sur ce coup, mais rien de perdu ! En renouvellant X fois ce genre d'expériences, tu ne peux à termes et statistiquement qu'y gagner, et grandir :-) !

1. Commiter proprement

    Des fois, tu vas réussir ton dev :-) : Tout roule comme tu veux :-) Et tu te dis qu'il te faut impérativement en faire profiter tout le monde, c'est normal, c'est instinctif chez les Hommes de bonnes volontrés... ;-)
    
    Alors, tu vas commit et proposer ton dev: Et un bon commit, c’est :

        Petit
        Clair
        Utile
        Avec un message explicite

      Exemples :

        feat: ajout du module d'analyse
        fix: correction du calcul de score
        docs: ajout section contribution

2. Faire une Pull Request (PR)

    La PR est le cœur de la collaboration. (Là, ça rigole plus car c'est maintenat que ton dev peut devenir 'officiel' :-))

    Avant de voir le détail de cette étape, juste, prenons du recul...:

    * T'as t'on demandé un diploume ?

    * Demandé pour qui tu te prends ? De quel droit tu te permets d'émettre un avis ?

    * Vérifier que t'es le fils à tel Papa, ou autre privilègié ?

    * À quelle dininité tu crois ?

    * Au fait, t'es plutôt caucasien, jaune, gris, brown...? vert ?:?

    → Non : **Ici, là et maintenant, TU ES TOI ! Et enfin, là, ici et maintenant, enfin au bon endroit !!! Seulement TOI, et TOI SEUL**, peut comprendre et accepter l'idée que **TON RÔLE est CAPITAL**, pas indispensable, juste CAPITAL **et IMPORTANT !**

    Concrètement, pour faire valoir ton dev, tu dois :

        Expliquer ce qui a été fait

        Expliquer pourquoi

        Mentionner les issues liées

        Être ouverte au dialogue

    Une PR n’est pas un examen.
    C’est une discussion technique entre humains bienveillants, et la scenette qui s'ajoute et fait qu'on aura ensemble un super film au final !

3. Participer aux revues de code

    Grâce à ton fork, puis clone, un simple Fetch et tu as le dernier apport le + top, et le + récent, d'un collaborateur, et ce, 24/24 - 7/7 et à volonté...

    Et relire le code des autres, c’est :

    * Apprendre

    * Aider facilement

    * Améliorer la qualité globale

    * Renforcer l’esprit d’équipe

    Les commentaires doivent être :

    * Constructifs

    * Respectueux
  
    Argumentés
  
    * Jamais condescendants

    * Raisonables
