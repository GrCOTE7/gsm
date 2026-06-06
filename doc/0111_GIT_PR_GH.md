<h3><div align='right'><span style="text-decoration:none;"><a href="./doc/0001_TOC.md" title="Table Of Content">TOC</a></span></div></h3>

<h1><div align='center'>11/12. GIT PR (SITE GH)</div></h1>

<h3 align="center">
  <a href="./0110_GIT_PR.md">← 0110_GIT_PR</a>
                     
  <a href="./0112_GIT_PR_DEAL.md">0112_GIT_PR_DEAL →</a>
</h3>

---

### 👉 PRÉAMBULE : À la moindre difficulté, consulte la **[page d'aide](./0000_HELPME.md)**

---

## PR via le site GitHub : objectif

Tu fais ton dev en local comme d'habitude, puis tu ouvres et gères la PR dans l'interface GitHub.

---

## 1. Prépare la branche en local

```bash
git branch --show-current
git push
```

Si c'est la première fois sur cette branche :

```bash
git push -u origin nom-de-ta-branche
```

---

## 2. Ouvre la page de PR sur GitHub

GitHub propose souvent le bouton **Compare & pull request** juste après le push.

CCC: Capture du bandeau GitHub avec le bouton "Compare & pull request".

Sinon, ouvre manuellement la comparaison entre :

- `base` = `GrCOTE7/gsm:main`
- `head` = `TonUserName/nom-de-ton-fork:nom-de-ta-branche`

CCC: Capture de l'ecran "Open a pull request" avec base/head visibles.

---

## 3. Rédige une PR utile

Titre conseillé (court et précis) :

```text
doc: corrige fautes et clarifie 0109/0110
```

Description conseillée :

```markdown
## But
Corriger des erreurs de formulation dans la doc Git.

## Changements
- correction orthographe dans 0109
- reformulation d'un passage ambigu

## Vérification
- lecture complete du chapitre
- liens internes verifies
```

CCC: Capture du formulaire PR rempli (titre + description + fichiers modifies).

Clique **Create pull request**.

CCC: Capture de la PR creee (numero, titre, etat Open).

---

## 4. Après ouverture : comment mettre à jour

Si review demandée :

1. Tu modifies ton code localement sur la meme branche
2. Tu commit
3. Tu push

```bash
git add .
git commit -m "doc: applique retours review"
git push
```

La PR se met à jour automatiquement.

CCC: Capture de l'onglet "Conversation" montrant un nouveau commit pousse sur la PR.

---

## 5. Erreurs fréquentes

### "J'ai commit sur main"

```bash
git switch -c fix/oups-commit-main
git push -u origin fix/oups-commit-main
```

Puis ouvre la PR depuis cette branche.

### "This branch has conflicts"

```bash
git fetch upstream
git rebase upstream/main
# ou git merge upstream/main
git push --force-with-lease   # uniquement si rebase
```

(*`--force-with-lease` est la version prudente du force push.*)

CCC: Capture de l'ecran GitHub indiquant "This branch has conflicts".

---

<h3 align="center">
  <a href="./0110_GIT_PR.md">← 0110_GIT_PR</a>
                     
  <a href="./0112_GIT_PR_DEAL.md">0112_GIT_PR_DEAL →</a>
</h3>
