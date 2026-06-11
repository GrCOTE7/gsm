<h3 align='right'><span style="text-decoration:none;"><a href="./0001_TOC.md" title="Table Of Content">TOC</a></span></h3>

<h1 align='center'>08/12. GIT DEEP - Conflits avancés</h1>

<h3 align="center">
  <a href="./0307_GIT_WORKTREE.md">← 0307_GIT_WORKTREE</a>
                     
  <a href="./0309_GIT_RESCUE.md">0309_GIT_RESCUE →</a>
</h3>

---

## Objectif

Résoudre les conflits proprement, vite, et sans casser l'intention du code.

---

## Dans Git Graph / VS Code

- Identifier exactement les fichiers en conflit
- Utiliser les options de résolution (`Current`, `Incoming`, `Both`)
- Relire le résultat final avant `continue`

---

## Équivalence CLI

```bash
# Pendant merge ou rebase
git status

# Après résolution
git add <fichier>
git merge --continue
# ou
git rebase --continue
```

Annuler si nécessaire :

```bash
git merge --abort
# ou
git rebase --abort
```

---

## Stratégie recommandée

1. Résoudre fichier par fichier
2. Rejouer un test rapide
3. Continuer l'opération

---

## Mini-exercice

1. Simule un conflit sur un même bloc
2. Résous-le dans VS Code
3. Termine en `--continue`
4. Compare avant/après dans Git Graph

---

<h3 align="center">
  <a href="./0307_GIT_WORKTREE.md">← 0307_GIT_WORKTREE</a>
                     
  <a href="./0309_GIT_RESCUE.md">0309_GIT_RESCUE →</a>
</h3>
