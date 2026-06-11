<h3 align='right'><span style="text-decoration:none;"><a href="./0001_TOC.md" title="Table Of Content">TOC</a></span></h3>

<h1 align='center'>02/12. GIT DEEP - Réécrire l'historique sans danger</h1>

<h3 align="center">
  <a href="./0301_GG_READ.md">← 0301_GG_READ</a>
                     
  <a href="./0303_GIT_CHERRY_PICK.md">0303_GIT_CHERRY_PICK →</a>
</h3>

---

## Objectif

Nettoyer tes commits avant PR sans casser le travail des autres.

---

## Dans Git Graph

Actions utiles (clic droit sur commit/branche):

- `Amend Commit` (corriger le dernier commit)
- `Rebase Current Branch on...` (rejouer proprement)
- `Interactive Rebase` (si dispo selon config)

Règle d'or :

- Réécris surtout des commits non partagés
- Si déjà push, préfère `--force-with-lease` au `--force`

---

## Équivalence CLI

```bash
# Corriger le dernier commit
git add .
git commit --amend

# Rebase interactif des 3 derniers commits
git rebase -i HEAD~3

# Push prudent après réécriture
git push --force-with-lease
```

---

## Plan anti-panique

Si tu as fait une bêtise d'historique :

```bash
git reflog
# puis revenir à un état sain
git reset --hard <id_reflog>
```

Utilise cette commande uniquement si tu sais ce que tu jettes localement.

---

## Mini-exercice

1. Fais 2 petits commits de test
2. Fusionne-les via rebase interactif (squash)
3. Vérifie dans Git Graph que l'historique est propre

---

<h3 align="center">
  <a href="./0301_GG_READ.md">← 0301_GG_READ</a>
                     
  <a href="./0303_GIT_CHERRY_PICK.md">0303_GIT_CHERRY_PICK →</a>
</h3>
