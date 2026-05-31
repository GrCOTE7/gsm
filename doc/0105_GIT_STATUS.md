<h3><div align='right'><span style="text-decoration:none;"><a href="./0001_TOC.md">TOC</a></span></div></h3>

<h1><div align='center'>GIT STATUS</div></h1>

<h3 align="center">
  <a href="./0104_GIT_BRANCH.md">← 0104_GIT_BRANCH</a>
                     
  <a href="./0106_GIT_COMMIT.md">0106_GIT_COMMIT →</a>
</h3>

---

*Avant de savoir où aller, savoir où l'on est et quand !*

*Et avant l'heure, c'est pas l'heure, et après l'heure, c'est plus l'heure...*

## 1. Position de ton projet en local (tes fichiers) VS ton dépôt distant (Sur GH)

Voyons tout de suite une autre commande souvent utile qui permet de faire le point :

```bash
git status
```

Elle vous donnera quelque chose comme :

### 1. Quelqu'un d'autre a déjà agît (Behind) 😁

```bash
On branch main
Your branch is behind 'origin/main' by 1 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)

nothing to commit, working tree clean
```

❌ On a déjà eût ce cas, et on l'avait [résolu directement sur GH](XXX)

Mais on peut aussi le faire + simplement, car normalement toujours prête, et ouverte, depuis / avec la CLI :

```bash
❌ 
```

### 2. Tout est à jour... (Up to date) ☹️

Ça paraît bien, mais ☹️, car ça veut aussi dire que vous n'avez sans doute pas encore changé ne serait-ce une virgule...

```bash
gsm> git status
On branch demo/mon_dev
Your branch is up to date with 'origin/demo/mon_dev'.

nothing to commit, working tree clean
```

Du coup, pas besoin de faire évoluer votre GH... 😭


### 3. Tu as déjà agît (Before) 😁

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
