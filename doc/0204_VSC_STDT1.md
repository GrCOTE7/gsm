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

### 👉 Pour avoir + simplement tous ceux qui nous intéressent : Édite ce fichier et ajoute à son contenu celui du fichier : [gsm/doc/files/keybindings.json](./files/keybindings.json)

Je ne sais plus trop quels items (paires clé-valeur) sont d'origine, donc ils sont dans l'ordre alphabétique, permettant un dédoublonnage + aisé.

💡 Et si toi, tu viens de poser ces settings dans un VSC 'tout neuf' (pas comme moi, qui depuis 2016 profite d'un système de centralisation des settings qui me repose instantanément tous mes réglages et extensions automatiquement à chaque nouvelle installation sur n'importe quelle machine), n'hésite pas à dédoublonner dans ce fichier ces settings proposés en ajout de ceux originaux, puis, tu connais maintenant... : **PR** ✌️ !

---

Tableau montrant, parmis les nouveaux raccourcis, ceux permettant d'avoir un émoji sémantique rapidement (Sémantique, parce que tu découvriras qu'ils ont un rôle réel dans notre système et ne sont pas là *que pour faire joli*...)

|      Raccourci     | Symbole |     Mnémonique     |
|:------------------:|:-------:|:-------------------|
| CTRL + ALT + **c** |    ❌   | **C**roix          |
| CTRL + ALT + **d** |  * [x]  | **D**one (fait)    |
| CTRL + ALT + **e** |    ↗️   | **E**xterne (Lien) |
| CTRL + ALT + **f** |    ✅   | **F**ait           |
| CTRL + ALT + **g** |    🎯   | **G**oal           |
| CTRL + ALT + **l** |    🦄   | **L**corne         |
| CTRL + ALT + **t** |  * [ ]  | **T**oDo           |
| CTRL + ALT + **v** |     ✔   | **V**alidé         |
| CTRL + ALT + **w** |    ⚠️   | **W**arning        |
| CTRL + ALT + **x** |    ☢️   | Rayons **X**       |

---

<h3 align="center">
  <a href="./0203_VSC_EXT3.md">← 0203_VSC_EXT3</a>
                     
  <a href="./0205_VSC_STDT2.md">0205_VSC_STDT2 →</a>
</h3>
