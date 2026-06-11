<h3 align='right'><span style="text-decoration:none;"><a href="./0001_TOC.md" title="Table Of Content">TOC</a></span></h3>

<h1 align='center'>05/12. GIT DEEP - Stash et commit partiel</h1>

<h3 align="center">
  <a href="./0304_GIT_BISECT.md">← 0304_GIT_BISECT</a>
                     
  <a href="./0306_GIT_TAG_RELEASE.md">0306_GIT_TAG_RELEASE →</a>
</h3>

---

## Objectif

Apprendre à séparer proprement plusieurs changements mélangés dans le même arbre de travail.

---

## Dans Git Graph

Git Graph permet de stasher rapidement via menu contextuel. Très pratique quand :

- tu dois changer de branche en urgence,
- ton travail n'est pas encore committable.

---

## Équivalence CLI

```bash
# Stash simple
git stash push -m "wip: correction en cours"

# Voir les stashes
git stash list

# Réappliquer
git stash apply stash@{0}
# ou réappliquer + supprimer
git stash pop
```

Commit partiel (ultra utile):

```bash
git add -p
git commit -m "fix: corrige uniquement le bug X"
```

`git add -p` te permet de choisir morceau par morceau ce qui entre dans le commit.

---

## Mini-exercice

1. Modifie 2 fichiers pour 2 sujets différents
2. Fais un commit partiel avec `git add -p` pour le sujet A
3. Stash le reste (sujet B)
4. Change de branche et réapplique le stash

---

<h3 align="center">
  <a href="./0304_GIT_BISECT.md">← 0304_GIT_BISECT</a>
                     
  <a href="./0306_GIT_TAG_RELEASE.md">0306_GIT_TAG_RELEASE →</a>
</h3>
