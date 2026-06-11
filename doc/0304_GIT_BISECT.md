<h3 align='right'><span style="text-decoration:none;"><a href="./0001_TOC.md" title="Table Of Content">TOC</a></span></h3>

<h1 align='center'>04/12. GIT DEEP - Trouver le commit qui casse (bisect)</h1>

<h3 align="center">
  <a href="./0303_GIT_CHERRY_PICK.md">← 0303_GIT_CHERRY_PICK</a>
                     
  <a href="./0305_GIT_STASH_PATCH.md">0305_GIT_STASH_PATCH →</a>
</h3>

---

## Objectif

Identifier vite le commit responsable d'un bug apparu "on ne sait quand".

---

## Point important

Git Graph aide à visualiser la zone suspecte, mais le vrai moteur de recherche ici, c'est la CLI `git bisect`.

Donc flux de travail idéal :

- visualiser dans Git Graph,
- exécuter bisect en terminal,
- revenir dans Git Graph pour comprendre et corriger.

---

## Procédure CLI

```bash
git bisect start
git bisect bad                 # commit actuel cassé
git bisect good <sha_ancien_ok>
```

Git te place sur un commit intermédiaire. Teste ton app :

```bash
git bisect good   # si OK
# ou
git bisect bad    # si KO
```

Répète jusqu'au commit fautif.

Fin obligatoire:

```bash
git bisect reset
```

---

## Mini-exercice

1. Prends une zone d'historique de 15-20 commits
2. Choisis un commit "bon connu"
3. Lance bisect jusqu'a trouver le "premier mauvais"

---

<h3 align="center">
  <a href="./0303_GIT_CHERRY_PICK.md">← 0303_GIT_CHERRY_PICK</a>
                     
  <a href="./0305_GIT_STASH_PATCH.md">0305_GIT_STASH_PATCH →</a>
</h3>
