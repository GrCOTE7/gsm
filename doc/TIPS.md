<!-- markdownlint-disable MD022 MD028 MD041 -->
<h3><div align='right'><span style="text-decoration:none;"><a href="./doc/0001_TOC.md" title="Table Of Content">TOC</a></span></div></h3>
<!-- markdownlint-enable MD041 -->

# Tips

## Ressources diverses

> [!NOTE] pour information

> [!TIP] pour conseil

> [!WARNING] pour risque

✅ pour confirmations

⚠️ pour alertes courtes

> [!NOTE]
> Astuce utile : ce bloc est mis en avant.

> [!TIP]
> Tu peux faire cela beaucoup plus simplement.

> [!WARNING]
> Attention, cette commande modifie le comportement du système.

### [https://flet.app/gallery/run/apps/icons_browser](https://flet.app/gallery/run/apps/icons_browser)

### [Emojis](https://emojipedia.org/fr/smileys)

Alternative : Extension VSC Markdown Emoji - Matt Bierner → CTRL + MAJ + E

# 😀 😉 😊 😁 🥳 👍 👌 👏 🙁 🤝 💙 ⚠️ ⌨️ 💻 🔍 📦  📋 📄 📂 🛠️ 🧰 🧵 🧪 🏛️ ⚡👉 📞 🎨 🚀 ✅ 🎯 ❌ 💡 🧱 📫 🧸 🚧 🏗️ 🥖 👨‍🍳 🧠 🌍 🤞 💪 ❤️ 🌐 🌱 🔄 🚨 📚 🙃 🔔

---

# 🐍 → serpent (emoji universel pour Python)
# 🔵🟡 → couleurs du logo Python
# 🐍💻 → Python + code
# 🐍⚙️ → Python + outils
# 🐍📦 → Python + packages

---

Git

# 🐙 GitHub
# 🔀 Versioning / branches / merge
# 🔀 (merge)
# 🔁 (sync)
# 🔂 (replay / rebase)
# 🌿 (branche)
# 🧵 (threads / commits)
# 🌳 Arbre de commits
# 🌱 (nouvelle branche)
# 🪢 (conflit)

# 🧰  (toolbox)
# 🛠️  (tools)
# 🧱  (building blocks)

🟦💻 VS Code
🧩🟦 VSC Ext
⌘⟦VS⟧

---

# ∃ ∄ ∀ ¬ ∧ ∨

<!-- ∃	&exist; - Il Existe
'Le "Symbole Il Existe", noté ∃, représente l''assertion qu''un élément existe dans le domaine de discours.'

∄	&#8708;
U+2204	Symbole de non-existence
Le Symbole de non-existence, noté ∄, est utilisé en logique formelle et en mathématiques pour indiquer qu'il n'existe aucun élément qui satisfait une propriété donnée.

∀	&forall; - Quel que soit
&#8704;
U+2200	Quantificateur Universel (Pour Tous)
Représente l'assertion qu'un prédicat est vrai pour tous les éléments dans le domaine.

¬	&not;
&#172;
U+AC	Symbole de Négation
Représente l'opération logique de négation, qui est vraie lorsque son opérande est faux et vice versa.

∧	&and;
&#8743;
U+2227	Symbole de Conjonction (ET)
Représente l'opération logique de conjonction, qui est vraie seulement lorsque ses deux opérandes sont vrais.

∨	&or;
&#8744;
U+2228	Symbole de Disjonction (OU)
Représente l'opération logique de disjonction, qui est vraie si au moins un de ses opérandes est vrai. 

// math: Div entière - dial: Par rapport à
O//o IMPORTANT

Afficher un tree propre et sans les __pycache__/ et leurs contenus :

Get-ChildItem -Recurse -Force -Directory |
    Where-Object { $_.FullName -notmatch "__pycache__" } |
    Tree

-->
Dans settings.json :

```json
 "markdownlint.config": {
    "MD028": false
  }
```
<!-- markdownlint-enable MD022 MD028 -->