# GIT - STATUS

## ← 4. [On attaque **le dev** ?](./0104_GIT_BRANCH.md)

## 5. GIT STATUS

*Avant de savoir où aller, savoir où l'on est et quand !*

*Et avant l'heure, c'est pas l'heure, et après l'heure, c'est plus l'heure...*

## → Synchro de ton dépôt distant (Sur GH) et de ton projet en local (tes fichiers)

Voyons tout de suite une autre commande souvent utile qui permet de faire le point :

```bash
git status
```

Elle vous donnera quelque chose comme :

### 1. Tout est à jour... ☹️

☹️, car ça veut dire aussi que vous n'avez pas encore changé ne serait-ce une virgule...

# ```bash
gsm> git status
XXX ds
```

Du coup, pas besoin de faire évoluer votre GH... 😭

### 2. quelqu'un d'autre à déjà agît 😁

```bash
On branch main
Your branch is behind 'origin/main' by 1 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)

nothing to commit, working tree clean
```

On a déjà eût ce cas, et on l'avait [résolu sur GH directement](XXX) : 

### 3. Vous avez déjà agît 😁

```bash
gsm> git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   doc/0104_GIT_DEV.md

no changes added to commit (use "git add" and/or "git commit -a")
gsm>
```
