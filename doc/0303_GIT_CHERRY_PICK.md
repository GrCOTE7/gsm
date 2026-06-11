<h3 align='right'><span style="text-decoration:none;"><a href="./0001_TOC.md" title="Table Of Content">TOC</a></span></h3>

<h1 align='center'>03/12. GIT DEEP - Cherry-pick propre</h1>

<h3 align="center">
  <a href="./0302_GIT_HISTORY_SAFE.md">← 0302_GIT_HISTORY_SAFE</a>
                     
  <a href="./0304_GIT_BISECT.md">0304_GIT_BISECT →</a>
</h3>

---

## Objectif

Récupérer UN commit utile sans merger toute une branche.

Cas typique:

- un hotfix fait sur une branche A,
- tu veux aussi ce fix sur branche B.

---

## Dans Git Graph

1. Repère le commit source
2. Clic droit sur le commit
3. `Cherry Pick this Commit`
4. Gère le conflit si besoin

Ensuite, contrôle le graphe et les fichiers modifiés.

---

## Équivalence CLI

```bash
# Se placer sur la branche cible
git switch ma-branche-cible

# Appliquer le commit
git cherry-pick <sha_commit>
```

En cas de conflit:

```bash
git status
git add <fichier_resolu>
git cherry-pick --continue
```

---

## À éviter

- Cherry-pick en chaîne de dizaines de commits
- Cherry-pick d'un merge commit sans comprendre l'impact

Si beaucoup de commits sont nécessaires, pense merge ou rebase.

---

## Mini-exercice

1. Crée une branche `fix/demo`
2. Fais un commit de correction
3. Cherry-pick ce commit sur `main` de test
4. Observe le résultat dans Git Graph

---

<h3 align="center">
  <a href="./0302_GIT_HISTORY_SAFE.md">← 0302_GIT_HISTORY_SAFE</a>
                     
  <a href="./0304_GIT_BISECT.md">0304_GIT_BISECT →</a>
</h3>
