<h3 align='right'><span style="text-decoration:none;"><a href="./0001_TOC.md" title="Table Of Content">TOC</a></span></h3>

<h1 align='center'>12/12. GIT PR - MISE EN APPLICATION (DEAL 🤝)</h1>

<h3 align="center">
  <a href="./0111_GIT_PR_GH.md">← 0111_GIT_PR_GH</a>
                     
  <a href="./0200_VSC_INSTALL.md">0200_VSC_INSTALL →</a>
</h3>

---

## DEAL : 🎯 Ta première vraie PR

**Objectif : Proposer une amélioration réelle**, même minuscule, **dans le dépôt GSM**.

Ce n’est pas qu'un exercice :

👉 Cette PR compte pour ton LV (LeVel - Niveau)

👉 Elle valide officiellement ta formation Git

👉 Elle te donne le droit d’ajouter **ton nom (ou pseudo) dans [le tableau d’honneur](./7777_SUIVIS.md)**

---

💡 Quel type d’amélioration ?

→ Tu choisis toi‑même ton sujet. L’important n’est pas la taille, mais l’utilité.

Quelques exemples parfaitement valides :

- corriger une faute d'orthographe dans un doc,
- clarifier une phrase ambiguë,
- corriger un lien cassé,
- améliorer un message utilisateur,
- ajouter une précision utile dans une page,
- dans le code, corriger un petit bug,
- améliorer un nom de variable, un commentaire, un log, etc.

Bref : une contribution réelle, utile, même minuscule.

---

## 🧭 Plan d’Action (court, efficace)

### 1. Crée une branche dédiée

```bash
  git switch -c doc/mon-premier-deal
```

### 2. Fais une petite amélioration utile

Relis une page, un script, un message…
Trouve un détail à améliorer → modifie-le.

### 3. Commit + push

```bash
  git add .
  git commit -m "doc: premiere contribution utile"
  git push -u origin doc/mon-premier-deal
```

### 4. Ouvre ta PR

Tu peux utiliser au choix la CLI ou l’interface GitHub (Comme ce que tu as vu dans les deux chapitres précédents respectivement).

---

## 🧰 Tips - Commande utile

* Erreur dans le message du commit

```bash
git commit --amend
```

→ Éditeur Vi ( ' i ' pour entrer en mode édition - ESC + ' :x ' pour quitter en enregistrant)

* Si le commit est déjà push :

```bash
git push --force-with-lease
```

---

## 🥳 Bravo, tu y es

Si ta PR est sur une branche dédiée, lisible, ciblée et utile, c'est gagné.

👉 **Tu as officiellement réussi ta formation Git.**

---

## 🎖️ Étape finale, ta récompense : **Ton pseudo dans le Tableau d'Honneur**

→ **Dès que ta PR est validée** (Acceptée par la communauté, c'est à dire que ton code, ta modification, se voit dans le dépôt upstream), tu as le droit d'apposer ton pseudo dans le **[Tableau d'Honneur](./7777_SUIVIS.md) ✌️** et de t'attribuer le Niveau **0200** 🎖️

1. Ajoute ton nom dans le [Tableau d'Honneur](./7777_SUIVIS.md) et ton Niveau
2. Fais immédiatement ta 2ᵉ PR pour valider aussi cette modification
3. **BRAVOs !** Tu rejoins officiellement les rangs des contributeurs efficaces du projet 🎉

---

<h3 align="center">
  <a href="./0111_GIT_PR_GH.md">← 0111_GIT_PR_GH</a>
                     
  <a href="./0200_VSC_INSTALL.md">0200_VSC_INSTALL →</a>
</h3>
