# GIT

## ← 3. [0103_GIT_USE](./0103_GIT_USE.md)

## 4. 🏗️ On attaque **le dev** ?

Juste pour te rassurer : Bon, jusqu'à maintenant, beaucoup de lecture pour bien comprendre et tout assimiler... Mais crois-moi: Si demain, tu dois tout recommencer, tu mettras max 2 minutes même si t'es pas doué 😉 ! Et ce principe sera toujours vrai 👍 - Bref, tu ne t'en aperçois p't'être même pas, mais tu d'viens bon 👌 ! Alors, courage pour la suite !

### .🎯 L’idée principale : Une ***BRANCH*** SPÉCIFIQUE pour le dev actuel courant

**Toujours oeuvrer dans une branche (*BRANCH* en anglais) dédiée** avant de commencer un développement spécifique. Cela garde un historique propre au moins sur la branche main, facilite les revues de code et évite donc de casser **la branche principale** (souvent **"main"** par défaut) qui **doit toujours rester stable**, au cas où... Et insdipensable pour un dev collaboratif.

    Pour info, une branche est comme une sorte d'autre copie intégrale du projet ! À ceci prêt que l'algorithme de GitHub (ou autre fournisseur) ne duplique pas vraiment tous les fichiers, mais garde 'simplement' en mémoire toutes les modifications, bref, quelques fichiers texte de quelques octets...
    
    Donc, très léger, mais surtout, ce traitement est complètement transparent pour nous : Alors, ne pas hésiter à en abuser !

### 🛠️ Donc, étape 1 — Crééer une branche de travail

Tu peux nommer ta branche comme tu veux, mais voici la [norme idéalement](https://codeheroes.fr/blog/git-comment-nommer-ses-branches-et-ses-commits) :

* Tout en minuscule, aucun accent
* pas d’espaces, utiliser des tirets - ou /
* refléter le type de travail (feature, fix, doc…) et le sujet du dev

Exemples de conventions :

* feature/new-service
* fix/bug-update-btn
* doc/upgrade-readme

Cela rend l’historique compréhensible et navigable pour toute l’équipe.

→ 🧩 C'est notre 2ème type de commande Git (On a déjà vu *clone*...)

En CLI, elle créée la branche 'upgrade/01_git-dev' et te pose dessus :

```bash
git branch upgrade/01_git-dev         # Créée la branche
git checkout upgrade/01_git-dev       # Passe sur la branche
    # OU - ménémonique, mais + court (et fais les 2 actions) :
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

Pour passer sur une autre branche (Par exemple, revenir sur la branche *main*) :

```bash
git checkout main
    # ET + moderne :
git switch main
    # À noter
git switch - # Retour sur la branche précédente (Pas forcément la main)
```

Voici qqes autre commandes très utiles liées aux branches

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

---

## → 5. [GIT STATUS](./0105_GIT_STATUS.md)
