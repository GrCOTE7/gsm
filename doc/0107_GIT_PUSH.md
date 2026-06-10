<h3><div align='right'><span style="text-decoration:none;"><a href="./doc/0001_TOC.md" title="Table Of Content">TOC</a></span></div></h3>

<h1><div align='center'>7/12. GIT PUSH ↑</div></h1>

<h3 align="center">
  <a href="./0106_GIT_COMMIT.md">← 0106_GIT_COMMIT</a>
                     
  <a href="./0108_GIT_EXO.md">0108_GIT_EXO →</a>
</h3>

---
  
La dernière étape du cycle des itérations locales (Souvenez-vous...)

<div align="center">
  <a href="./imgs/301_GIT.png" target="_blank">
    <img src="./imgs/301_GIT.png" width="700">
  </a>
</div>

## Synchronisation de ton projet en local (tes fichiers) et de ton dépôt distant (Sur GH)

Alors, comme ça... **Tu as agît**...? Codé, fait des commits... **B R A V O S !**

Et du coup, voyons ce que 'raconte' *git status*... :

```bash
gsm> git status
On branch main
Your branch is ahead of 'upgrade/01_git-dev' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
gsm>
```

Maintenant, afin que ce que tu as fait et codé compte vraiment, il faut, comme le suggère la CLI, '***push***' tes *commits*.

C'est l'étape **la plus importante**, celle qui rend 'ton travail enregistré dans le marbre' !

## 🚀 La commande clé pour pousser vers ton fork

```bash
git push
```

Elle est correcte **à condition** que :

- Ta branche locale main soit bien liée à ***origin/main***,
- ton remote origin pointe bien vers ton dépôt GitHub,
- tu aies les droits d’écriture (ce qui est le cas ici, vu que tu es dans ton *fork*).

### 👉 *Même si tu découvriras bientôt des outils qui simplifient complètement, rendent rapides, intuitives et ludiques ces commandes car applicables 'à simples coups de souris', il est toujours bon et parfois même salvateur de connaître les commandes de base en console.*

* [ ] Cf. si besoin de précisions pour la clé SSH

---

<h3 align="center">
  <a href="./0106_GIT_COMMIT.md">← 0106_GIT_COMMIT</a>
                     
  <a href="./0108_GIT_EXO.md">0108_GIT_EXO →</a>
</h3>
