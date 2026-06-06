<h3><div align='right'><span style="text-decoration:none;"><a href="./doc/0001_TOC.md" title="Table Of Content">TOC</a></span></div></h3>

<h1><div align='center'>10/10. GIT PR</div></h1>

<h3 align="center">
  <a href="./0109_GIT_SYNC.md">← 0109_GIT_SYNC</a>
                     
  <a href="./0201_VSC_INSTALL.md">0201_VSC_INSTALL →</a>
</h3>

---

### 👉 PRÉAMBULE : À la moindre difficulté, consulte la **[page d'aide](./0000_HELPME.md)**

---

Tu vas voir qu'une PR, ce n'est pas "un truc de senior" : c'est juste une méthode propre pour proposer une amélioration.

---

## ***Pull Request*** (PR) ou comment proposer ton travail proprement dans le dépôt *upstream*

Une **PR** est une demande de fusion de ton code vers le dépôt cible.

Dans notre contexte GSM :

- Tu développes sur ton **fork**,
- tu pushes ta branche de dev sur ton fork,
- puis tu demandes à fusionner cette branche vers le dépôt **upstream**.

---

## Avant de créer la PR : Mini check

Dans ta branche de travail (pas `main`), vérifie :

```bash
git status
git log --oneline -n 5
```

Tu dois idéalement avoir :

- un arbre propre (`working tree clean`),
- des commits clairs,
- une branche bien nommée (`fix/...`, `doc/...`, `feature/...`).

Si ta branche n'est pas encore sur GH :

```bash
git push -u origin nom-de-ta-branche
OU, comme tu as fork, cela suffit :
git push
```

Le `-u` crée le lien local <-> distant. Ensuite, un simple `git push` suffit.

---

## Méthode A (recommandée) : Git en CLI + création PR sur le site GitHub

### 1. Vérifie ta branche active

```bash
git branch --show-current
```

### 2. Push ta branche

```bash
git push
```

Si c'est la première fois sur cette branche :

```bash
git push -u origin nom-de-ta-branche
```

### 3. Ouvre la page de comparaison GitHub

GitHub propose souvent un bouton **Compare & pull request** juste après le push.

CCC: Capture du bandeau GitHub avec le bouton "Compare & pull request".

Sinon, ouvre manuellement la comparaison entre :

- `base` = `GrCOTE7/gsm:main`
- `head` = `TonUserName/nom-de-ton-fork:nom-de-ta-branche`

CCC: Capture de l'ecran "Open a pull request" avec base/head visibles.

### 4. Rédige une PR utile

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

## Verification
- lecture complete du chapitre
- liens internes verifies
```

CCC: Capture du formulaire PR rempli (titre + description + fichiers modifies).

### 5. Crée la PR

Clique **Create pull request**.

CCC: Capture de la PR creee (numero, titre, etat Open).

---

## Méthode B : création de PR en CLI avec GitHub CLI (optionnelle)

Si `gh` est installé :

```bash
gh --version
```

Créer une PR directement en CLI :

```bash
gh pr create \
  --base main \
  --head TonUserName:nom-de-ta-branche \
  --title "doc: corrige fautes et clarifie 0109/0110" \
  --body "Corrections de doc + clarifications mineures."
```

Puis lister/ouvrir :

```bash
gh pr list
gh pr view --web
```

CCC: Capture du retour CLI de `gh pr create` avec URL de la PR.

---

## Après ouverture de la PR : le cycle normal

Une PR n'est pas figée. Si on te demande des ajustements :

1. Tu modifies ton code localement sur **la meme branche**
2. Tu commits
3. Tu pushes

```bash
git add .
git commit -m "doc: applique retours review"
git push
```

La PR se met à jour automatiquement.

CCC: Capture d'un onglet "Conversation" montrant un nouveau commit pousse sur la PR.

---

## Bonnes pratiques PR (important)

- 1 PR = 1 sujet (petite, lisible, testable)
- Préfère plusieurs petites PR qu'une enorme PR confuse
- Titre explicite (`fix:`, `doc:`, `feat:`)
- Description avec "But / Changements / Verification"
- Reste courtois en review, la critique vise le code, jamais la personne

---

## Erreurs fréquentes (et correction rapide)

### "J'ai commit sur main"

Crée une branche depuis ton état actuel puis pousse-la :

```bash
git switch -c fix/oups-commit-main
git push -u origin fix/oups-commit-main
```

Ensuite, ouvre la PR depuis cette branche.

### "Ma branche a des conflits"

Synchronise-la avec `main` puis résous les conflits :

```bash
git fetch upstream
git rebase upstream/main
# ou git merge upstream/main
git push --force-with-lease   # uniquement si rebase
```

(*Le `--force-with-lease` est la version prudente du force push.*)

CCC: Capture de l'ecran GitHub indiquant "This branch has conflicts".

---

## Résumé express

```bash
# 1) creer branche
git switch -c doc/ma-premiere-pr

# 2) coder
# ...

# 3) commit
git add .
git commit -m "doc: ma premiere contribution"

# 4) push
git push -u origin doc/ma-premiere-pr

# 5) ouvrir PR (site GH ou gh pr create)
```

> 🎯 Objectif atteint quand ta PR est ouverte, lisible, et facile a relire.

Chaque petite PR propre fait avancer le projet, et te fait progresser tres vite.

---

### Mettre en pratique est une nécessité absolue

### → 💡 Deal : Ton premier objectif concret est simple

Corrige ne serait-ce qu'une virgule dans la doc, et propose ta **première PR**.

---

<h3 align="center">
  <a href="./0109_GIT_SYNC.md">← 0109_GIT_SYNC</a>
                     
  <a href="./0201_VSC_INSTALL.md">0201_VSC_INSTALL →</a>
</h3>

