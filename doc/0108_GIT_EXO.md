<h3><div align='right'><span style="text-decoration:none;"><a href="./doc/0001_TOC.md" title="Table Of Content">TOC</a></span></div></h3>

<h1><div align='center'>🚧 8/10. GIT EXO - T.P. - Exercice 🏗️</div></h1>

<h3 align="center">
  <a href="./0107_GIT_PUSH.md">← 0107_GIT_PUSH</a>
                     
  <a href="./0109_GIT_SYNC.md">0109_GIT_SYNC →</a>
</h3>

---

Pour comprendre l'importance et la magie du Git, voyons un exemple exagéré à l'extrême :

Imaginons que fatigué, tu effaces par erreur tout un dossier important...
Sans le git, cela serait assurément catastrophique, on ne sauvegarde pas toutes les 2 minutes !!!

Donc, révisons l'ensemble de ce que nous avons vu, et agissons en PRO; Travaillons sur une nouvelle branche spécifique bien nommée que nous créons pour l'occasion :

## On attaque le dev → Création d'une branche spécifique

```bash
git checkout -b exo/action_folle
OU, + moderne :
git switch -c exo/action_folle
```

## On code, mais là... mal

Mais pour l'exemple, on va volontairement créer un problème pour s'entraîner.

Imaginons un cas gravissime : on efface un dossier clé de l'app, `src/upu`. (Il n'y a pas plus critique, c'est tout le cœur de l'app !!!)

<img src="./imgs/win_logo.png" width='18'> Windows (PowerShell):

```bash
Remove-Item -Recurse -Force .\src\upu
```

<img src="./imgs/linux_logo.png" width='18'> Linux / macOS:

```bash
rm -rf src/upu
```

## Et qu'en plus, on ne le voit pas tout de suite, donc on valide notre dev

On valide la catastrophe locale 😭 - On l'aurait jamais fait si on avait fait un simple :

```bash
git status
```

Et on simule l'enregistrement Git de l'erreur complète :

```bash
git add .
git commit -m "feat: grosse refacto - nettoyage du code" # snif
```

## 1er cas : on s'en aperçoit juste après le add et le commit

Si l'erreur est détectée juste après ton commit local (pas encore poussé), tu peux revenir proprement en arrière.

Option A : Tu veux garder les changements dans les fichiers pour les corriger (ça annule le commit, mais pas le add)

```bash
git reset --soft HEAD~1
```

Option B : Tu veux annuler le commit mais garder les changements non indexés (Soit, annuler le commit, ET le add - Mais le dossier reste effacé)

```bash
git reset --mixed HEAD~1
```

Ensuite, si les fichiers concernés ne sont plus indexés, on peut restaurer alors uniquement le dossier supprimé par erreur, tout en gardant d'autres changement qu'on aurait pû faire par ailleurs :

```bash
git reset --mixed HEAD~1
```

Puis " re *commit* " proprement si d'autres changements avaient été faits :

```bash
git add .
git commit -m "fix: restauration du dossier supprimé par erreur"
```

## 2e cas : On s'en aperçoit après le push sur le dépôt distant

Si le commit est déjà poussé, évite de réécrire l'historique partagé.
Le plus simple et le plus propre est de faire un commit de correction.

```bash
# Restaurer le dossier depuis le commit précédent
git restore --source=HEAD~1 src/upu
git add src/upu
git commit -m "fix: restauration du dossier supprimé par erreur"
git push
```

Alternative (quand on veut complè-tement annuler exactement un commit précis - ne sera plus dans l'historique):

```bash
git log --oneline
git revert <sha_du_commit_fautif>
git push
```

`git revert` crée un nouveau commit qui annule proprement le commit cible, sans casser l'historique distant.

## 3e cas : On est complètement perdu

On ne sait plus du tout où on en est 🫨...

Heureusement, on a dev sur une autre branche que `main`...

Objectif : Se remettre dans un état propre, puis reprendre calmement.

1. Vérifie la situation

```bash
git status
git branch
git log --oneline --decorate -n 10
```

2. Sauvegarde de ce qui traîne (au cas où)

```bash
git stash push -u -m "sauvegarde avant nettoyage exo/action_folle"
```

3. Reviens sur la branche principale

```bash
git switch main
git pull
```

4. Supprime la branche d'exercice locale

```bash
git branch -D exo/action_folle
```

5. (Optionnel) Supprime aussi la branche distante

```bash
git push origin --delete exo/action_folle
```

6. Repars proprement

```bash
git switch -c exo/bonne_action
```

## Fin de l'exercice

Tu viens de voir les 3 réflexes qui sauvent en pratique. Fais-les réellement :

- Erreur locale après commit : `git reset` puis `git restore`
- Erreur déjà poussée : commit de correction ou `git revert`
- Panique totale : `git stash`, retour sur `main`, nettoyage de branche, puis nouveau départ

**Le vrai super-pouvoir de Git, ce n'est pas de ne jamais se tromper. C'est de pouvoir se tromper sans tout perdre.**

---

<h3 align="center">
  <a href="./0107_GIT_PUSH.md">← 0107_GIT_PUSH</a>
                     
  <a href="./0109_GIT_SYNC.md">0109_GIT_SYNC →</a>
</h3>
