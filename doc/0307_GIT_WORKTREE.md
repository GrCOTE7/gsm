<h3 align='right'><span style="text-decoration:none;"><a href="./0001_TOC.md" title="Table Of Content">TOC</a></span></h3>

<h1 align='center'>07/12. GIT DEEP - Worktree</h1>

<h3 align="center">
  <a href="./0306_GIT_TAG_RELEASE.md">← 0306_GIT_TAG_RELEASE</a>
                     
  <a href="./0308_GIT_CONFLICTS_DEEP.md">0308_GIT_CONFLICTS_DEEP →</a>
</h3>

---

## Objectif

Travailler sur plusieurs branches en parallèle sans tout stasher en permanence.

---

## Pourquoi c'est puissant

Avec `git worktree`, tu peux avoir:

- une fenêtre pour la feature,
- une fenêtre pour un hotfix urgent,
- le tout dans le même dépôt.

---

## Équivalence CLI (principal)

```bash
# Ajouter un worktree sur une branche
git worktree add ../gsm-hotfix hotfix/urgent

# Lister
git worktree list

# Retirer quand terminé
git worktree remove ../gsm-hotfix
```

---

## Lien avec Git Graph

Git Graph visualise très bien les branches, mais la création/gestion de worktree reste surtout plus directe en CLI.

---

## Mini-exercice

1. Crée un worktree `../gsm-hotfix`
2. Fais un commit de test dedans
3. Vérifie le commit dans Git Graph
4. Supprime le worktree

---

<h3 align="center">
  <a href="./0306_GIT_TAG_RELEASE.md">← 0306_GIT_TAG_RELEASE</a>
                     
  <a href="./0308_GIT_CONFLICTS_DEEP.md">0308_GIT_CONFLICTS_DEEP →</a>
</h3>
