<h3 align='right'><span style="text-decoration:none;"><a href="./0001_TOC.md" title="Table Of Content">TOC</a></span></h3>

<h1 align='center'>10/12. GIT DEEP - Limites de Git Graph</h1>

<h3 align="center">
  <a href="./0309_GIT_RESCUE.md">← 0309_GIT_RESCUE</a>
                     
  <a href="./0311_GIT_DEEP_EXO.md">0311_GIT_DEEP_EXO →</a>
</h3>

---

## Objectif

Savoir quand rester en GUI (GG) et quand passer en CLI sans perdre de temps.

---

## Git Graph excelle pour

- Visualiser l'historique,
- inspecter commits et diffs,
- actions courantes (checkout, merge, cherry-pick, tag selon cas).

## CLI reste meilleure pour

- `bisect`,
- `reflog` et opérations de secours,
- automatisation et scripts,
- commandes très fines (rebase avancé, plumbing, etc.).

---

## Règle pratique

- Si opération simple + visuelle : Git Graph
- Si diagnostic profond + répétition : GG + CLI + GG
- Si doute : Fais d'abord une lecture dans Git Graph, puis exécute en CLI

---

## Mini-exercice

1. Prends 3 opérations de ton quotidien Git
2. Classe-les GUI ou CLI
3. Justifie le choix en 1 phrase

---

<h3 align="center">
  <a href="./0309_GIT_RESCUE.md">← 0309_GIT_RESCUE</a>
                     
  <a href="./0311_GIT_DEEP_EXO.md">0311_GIT_DEEP_EXO →</a>
</h3>
