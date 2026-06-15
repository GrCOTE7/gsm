<h3 align='right'><span style="text-decoration:none;"><a href="./0001_TOC.md" title="Table Of Content">TOC</a></span></h3>

<h1 align='center'>VSC - Extensions Organisationnelles - STDT 1</h1>

<h3 align="center">
  <a href="./0203_VSC_EXT3.md">← 0203_VSC_EXT3</a>
                     
  <a href="./0205_VSC_STDT2.md">0205_VSC_STDT2 →</a>
</h3>

---

## Notre système : **STDT** - **S**hortcuts + **T**o**D**o **T**ree → **[Efficience](https://fr.wikipedia.org/wiki/Efficience) GARANTIE !**

Les "ToDo list", tu connais... Tu en as peut-être même "codé le code", une appli dans le cadre de l'apprentissage d'un langage ou autre...

Mais pour nous, cette extension complétée de réglages va nous permettre de gagner énormément en efficience !

En effet, quand on code, une bonne partie de notre temps consiste à toujours apprendre... On en lit, des signatures, on en voit, des exemples, etc...

Mais du coup, ça peut éveiller en nous plusieurs choses :

- Dans une doc, on tombe sur une notion qu'on aimerait bien approfondir pour X raisons,
- Et dans notre réflexion, la pensée d'autres choses à absolument tester au + vite...

Bref, sans parler de notifs, ou encarts qu'on voit par ci, par là... Autant de fortes raisons d'être vite divertis et d'en perdre complètement le fil de notre objectif initial ! Car en +, si on ne creuse pas de suite, on garde aussi la peur de perdre une info, peut-être cruciale, d'une ressource précieuse...

Notre système **S**hortcut + **T**o**D**o **T**ree est la **Solution Optimale** !

Et **la lecture de cette page et des deux suivantes va te l'offrir intégralement !**

→ [Yoda](https://fr.wikipedia.org/wiki/Yoda) te dirait : *Et en +, t'ennuyer plus jamais tu ne connaîtras !*

## Élément 1 : ShortCuts - Raccourcis (Json)

### ⚠️ ATTENTION: Uniquement pour VSC sur Win

### Pour Codespaces, utiliser les snippets (voir tableau ci-dessous)

Là, il ne s'agit pas vraiment d'une extension ([Bien que si tu cliques là, sur 'ces mots bleus', celle de la page qui s'ouvrira t'apporte des raccourcis spécifiques pour les docs rédigées en MarkDown](https://marketplace.visualstudio.com/items?itemName=mdickin.markdown-shortcuts)), car nous parlons là davantage d'une fonctionnalité native de VSC.

En effet, d'emblée, de nombreux raccourcis (claviers → *keybindings*) existent :

<div align="center">
  <a href="./imgs/204_vsc1_shortcuts.png" target="_blank">
    <img src="./imgs/204_vsc1_shortcuts.png" width='400' title='Shortcuts' alt='Shortcuts Preview'>
  </a>
</div>

Tu peux en trouver un précis, soit en tapant son nom, soit sa combinaison de touches :

<div align="center">
  <a href="./imgs/204_vsc2_shortcuts.png" target="_blank">
    <img src="./imgs/204_vsc2_shortcuts.png" width='400' title='Shortcuts' alt='Shortcuts Preview'>
  </a>
</div>

Donc, tu dois voir que ce tableau est plutôt long, très long... (Il faut préciser qu'y sont aussi référencés tous les raccourcis des extensions déjà installées...)

Et pourtant, les raccourcis qui nous intéressent aujourd'hui ne sont même pas dans ce tableau !!! En effet, il y a une autre liste de raccourcis 'customs' (personnels), mais cette fois sous forme d'un fichier `.json` :

### 👉 Pour éditer ce fichier : **CTRL + MAJ + P** et saisir quelques lettres

<div align="center">
  <a href="./imgs/204_vsc3_shortcuts.png" target="_blank">
    <img src="./imgs/204_vsc3_shortcuts.png" width='400' title='Shortcuts' alt='Shortcuts Preview'>
  </a>
</div>
<br>

Et voici comment en ajouter un : Exemple : **CTRL + ALT + x** → ' ☢️ '

<div align="center">
  <a href="./imgs/204_vsc4_shortcuts.png" target="_blank">
    <img src="./imgs/204_vsc4_shortcuts.png" width='400' title='Shortcuts' alt='Shortcuts Preview'>
  </a>
</div>

### 👉 Pour avoir + simplement tous ceux qui nous intéressent

Dans GSM, on personalise les raccourcis personnalisés (le fichier json) pour notre VSC local, et des code-snippets pour celui dans Codespaces :

Notre VSC se base sur les 2 fichiers correcpondants situés dans ./vscode/

- Raccourcis dans [../.vscode/keybindings.json](../.vscode/gsm.code-snippets)

  → Copier le contenu dans votre fichier json comme vu dans la capture précédente.

- snippets dans [../.vscode/gsm.code-snippets](../.vscode/gsm.code-snippets)

  Là, rien à faire, notre installateur de codespace viendra les chercher ci 😉 !

Donc, si tu veux ajouter ou corriger une insertion utile à la communauté :

1. Modifie Le fichier correspondant,
2. teste le raccourci dans ton VSCode local, ou le snippet dans COdeSpace,
3. Et ouvre alors une PR courte avec le changement et décrit son intérêt.

---

## Tablau récapitulatif des raccourcis

⚠️ : Pour le code du snippet, faire **TAB** après le code.

| Raccourci<br>(Local) | Snippet<br>(Codespace)   | Commentaire | Coloré | Symbole   | Signification                     | STDT  |
|:--------------------:|:------------------------:|:-----------:|:------:|:---------:|:---------------------------------:|:-----:|
| CTRL + ALT + **c**   | **redcross** ou **rc**   | -           | ✔      | ❌        | **C**roix Rouge- Urgence          |   ✔   |
| CTRL + ALT + **x**   | **xray** ou **rad**      | -           | ✔      | ☢️        | **X** Ray → Dangereux             |   ✔   |
| -                    | -                        | **2fix**    | ✔      | -         | To fix → À règler                 |   ✔   |
| -                    | -                        | **2dbug**   | ✔      | -         | To debug → À corriger             |   ✔   |
| -                    | -                        | **XXX**     | ✔      | -         | Posé provisoirement               |   ✔   |
| -                    | -                        | **2ar**     | ✔      | -         | To Remove→ À remove - À enlever   |   ✔   |
| -                    | -                        | **2see**    | ✔      | -         | To see → À voir                   |   ✔   |
| -                    | -                        | **2let**    | ✔      | -         | To let → À laisser                |   ✔   |
| -                    | -                        | **2do**     | ✔      | -         | To do → À faire                   |   ✔   |
| CTRL + ALT + **t**   | **todo** ou **td**       | -           | ✔      | \* [ ]    | **T**oDo → À faire - En liste     |   ✔   |
| CTRL + ALT + **a**   | **actuel**, **ec**       | -           | ✔      | \* [-]    | ToDo **A**ctuelle → En Cours      |   ✔   |
| CTRL + ALT + **d**   | **done** ou **dx**       | -           |        | \* [x]    | ToDo **D**one → **f**aite         |   -   |
| CTRL + ALT + **l**   | **gc7** ou **licorne**   |             | ✔      | 🦄        | **L**icorne - ToDo réservé        |   ✔   |
| CTRL + ALT + **g**   | **goal** ou **obj**      |             | ✔      | 🎯        | **G**oal → But                    |   ✔   |
| CTRL + ALT + **e**   | **ext** ou **elk**       |             | ✔      | ↗️        | **E**xtérieur - Lien              |   -   |
| CTRL + ALT + **v**   | **valid** ou **val**     |             | ✔      | ✔         | **V**alide                        |   -   |
| CTRL + ALT + **p**   | **pin**, **note**        |             | ✔      | 📌        | **P**in → Attache                 |   -   |
| CTRL + ALT + **y**   | **ok**, **oui**, **yes** |             | ✔      | ✅        | **Y**es → Oui                     |   -   |
| CTRL + ALT + **n**   | **nok**, **non**, **no** |             | ✔      | 🟥        | **N**o → Non                      |   -   |
| CTRL + ALT + **w**   | **warn** ou **warning**  |             | ✔      | ⚠️        | **W**arning → Attention !         |   -   |
| CTRL + ALT + **b**   | **bad** ou **interdit**  |             | ✔      | ⛔        | **B**ad - Interdit                |   -   |

En commentaire, cela colore la ligne pour la mettre bien en évidence.

En STDT (Notre système Shortcuts - ToDo Tree), un ✔ veut juste dire le tag est comptabilisé par ToDo Tree (Visible en bas, dans la barre d'état).

❌ vérif tous snippets

<h3 align="center">
  <a href="./0203_VSC_EXT3.md">← 0203_VSC_EXT3</a>
                     
  <a href="./0205_VSC_STDT2.md">0205_VSC_STDT2 →</a>
</h3>
