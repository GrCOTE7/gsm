<h3><div align='right'><span style="text-decoration:none;"><a href="./doc/0001_TOC.md" title="Table Of Content">TOC</a></span></div></h3>

<h1><div align='center'>GIT STATUS</div></h1>

<h3 align="center">
  <a href="./0104_GIT_BRANCH.md">← 0104_GIT_BRANCH</a>
                     
  <a href="./0106_GIT_COMMIT.md">0106_GIT_COMMIT →</a>
</h3>

---

*Avant de savoir où aller, savoir où l'on est et quand !* *Et comme avant l'heure, c'est pas l'heure, et qu'après l'heure, c'est plus l'heure...*

## 1. Position de ton projet en local (tes fichiers) VS ton dépôt distant (Sur GH)

Voyons tout de suite une commande souvent utile ouisqu'elle permet de faire le point :

```bash
git status
```

Elle vous donnera quelque chose comme :

### 1. " Quelqu'un d'autre " a déjà agît... Tu es ***Behind*** - En retard sur ton dépôt GH 😁

Cela peut te surprendre, vu qu'on parle là, de ton dépôt distant, sur GH, et qu'à priori, pour l'instant, tu n'as sans doute encore pas trop partager le lien de ton repository...

Mais en fait, cela peut quand même probablement t'arriver... Mais ce ne serait pas forcément quelqu'un d'autre... Que toi !

En effet, il peut t'arriver de rapidement vouloir mettre à jour un détail (ou +) depuis un codespace de ton fork...

**Dans ce code source** ci-dessous, tu connais la musique maintenant, **remplace MP21170 par ton UserName GH** pour y avoir TON badge et clique dessus ! 

<br>
<div align='center'>
  <a href="https://codespaces.new/MP21170/gsm" title="Open YOUR CodeSpace Now... Click HERE!">
      <img src="https://img.shields.io/badge/Github%20Codespace%20Ready-green.svg" alt="CodeSpace link" />
  </a>
</div>
<br>

Comme tu l'auras lu dans le README, tu peux y voir ton code 'comme à la maison', dans ton éditeur, et même y lancer le script !!!

Mais tu verras que tu peux mettre y faire commits, et push !!!

Donc, ce sera en gros le moyen de mettre de suite à jour ton GH, avant même ton dépôt local ! @ retenir !

Ou encore, plus tard, il suffit que toi ou un collègue push depuis un autre compte GH à qui tu auras accordé les droits d'accès, codespace ou pas !...

Dans tous ces cas, tu verras quelque chose comme :

```bash
On branch upgrade/01_git-dev
Your branch is behind 'upgrade/01_git-dev' by 1 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)

nothing to commit, working tree clean
```

Alors, **il suffit de faire ce que recommande la CLI** :

```bash
git pull
```

### → 💡Note que tu peux aussi appliquer ces commandes sur la branche main...

D'ailleurs, dans l'idéale, comme tu es censé ne jamais travailler dans la *main*, tu ne dois donc logiquement en conséquences n'y faire que ces commandes... 😉

→ À l'issue, tu auras ce genre de réponse de la commande 😊 (Le nom de ta branche pouvant bien évidement varier selon ton dev... ;-) 😉) :

### 2. Tout est à jour... (Tu es ***Up to date***) ☹️

Ça paraît bien, mais ☹️, car ça veut aussi dire que vous n'avez sans doute pas encore changé ne serait-ce une virgule...

```bash
gsm> git status
On branch upgrade/01_git-dev
Your branch is up to date with 'origin/upgrade/01_git-dev'.

nothing to commit, working tree clean
```

Du coup, pas besoin de faire évoluer votre GH... 😭

### 3. Tu as déjà agît (Tu es ***Before*** - En avance sur ton dépôt GH) 😁

```bash
gsm> git status
On branch upgrade/01_git-dev
Your branch is up to date with 'origin/upgrade/01_git-dev'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   doc/0105_GIT_STATUS.md

no changes added to commit (use "git add" and/or "git commit -a")
gsm>
```

Bravo, tu as déjà codé, et il te faut donc simplementfaire un ***commit* + *push*** sur ton dépôt GH... On va voir cela maintenat 👍 :

(Dans notre exemple ci-dessus, de la saisie dans cette page)

---

<h3 align="center">
  <a href="./0104_GIT_BRANCH.md">← 0104_GIT_BRANCH</a>
                     
  <a href="./0106_GIT_COMMIT.md">0106_GIT_COMMIT →</a>
</h3>
