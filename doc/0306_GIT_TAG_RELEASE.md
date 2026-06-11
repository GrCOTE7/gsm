<h3 align='right'><span style="text-decoration:none;"><a href="./0001_TOC.md" title="Table Of Content">TOC</a></span></h3>

<h1 align='center'>06/12. GIT DEEP - Tags et Releases</h1>

<h3 align="center">
  <a href="./0305_GIT_STASH_PATCH.md">← 0305_GIT_STASH_PATCH</a>
                     
  <a href="./0307_GIT_WORKTREE.md">0307_GIT_WORKTREE →</a>
</h3>

---

## Objectif

Marquer une version stable de façon propre, reproductible et partageable.

---

## Dans Git Graph

Depuis un commit stable (souvent sur `main`):

1. Clic droit sur le commit
2. `Create Tag`
3. Nommer le tag (`v1.2.0`)
4. Push du tag vers le dépôt distant

---

## Équivalence CLI

```bash
# Tag annoté
git tag -a v1.2.0 -m "release: v1.2.0"

# Envoyer les tags
git push origin v1.2.0
# ou tout envoyer
git push --tags
```

---

## Bonnes pratiques

- Utiliser SemVer ou Semantic-release (`MAJOR.MINOR.PATCH`)
- Taguer seulement des commits vérifiés
- Garder une note de version claire

---

## Mini-exercice

1. Choisis un commit stable
2. Crée le tag `v0.0.1-test`
3. Push le tag
4. Vérifie sa présence sur GitHub

---

<h3 align="center">
  <a href="./0305_GIT_STASH_PATCH.md">← 0305_GIT_STASH_PATCH</a>
                     
  <a href="./0307_GIT_WORKTREE.md">0307_GIT_WORKTREE →</a>
</h3>
