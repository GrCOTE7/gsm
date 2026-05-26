# GIT

## ← 4. [On attaque **le dev** ?](./0104_GIT_BRANCH.md)

## 5. GIT STATUS

## IMPORTANT : C'est la synchro de ton dépôt distant (Sur GH) et de ton projet en local (tes fichiers)

Voyons tout de suite un autre commande souvent utile :

```bash
git status
```

Elle vous donnera quelque chose comme :

### Tout est à jour... ☹️

☹️, car ça veut dire aussi que vous n'avez pas encore changé ne serait-ce une virgule...

```bash
gsm> git status
❌ ...
```

Du coup, pas besoin de faire évoluer votre GH... 😭


### Vous avez déjà agît 😁


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
