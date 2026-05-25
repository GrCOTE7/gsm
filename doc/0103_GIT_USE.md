# GIT

## ← [0102_GIT_CLONE](./0102_GIT_CLONE.md)

## 3. Installe les dépendances si nécessaire et lance l'app

Déjà, depuis le dossier où l'on a exécuté le clône, on 'rentre en CLI' (Rappel : = Console) et maintenant dans le dossier du projet **gsm/**

```bash
cd gsm
```

Et l'install des libs, et le run, tout cela se fait normalement en une seule commande ! 💪

```bash
uv run flet run
```

👉 À noter: Sur Win, il existe même un raccourci... (... Encore + court !!! Lol) à exécuter en CLI à la racine :

```bash
./go
```

💡 Tous linuxien et MacOxien sont invités à compléter ces docs pour adapter ces helpers sur ces Mc et bien-sûr, faire les **PR** qui s'imposent alors...

## Teste que l'app marche au moins pour TOI, en local (Et sinon: CHAT, [ISSUE](https://github.com/GrCOTE7/gsm/issues/new/choose) bref, plan [ORSEC](https://fr.wikipedia.org/wiki/Dispositif_ORSEC)!!! Heu... Simplement **[page d'aide](./0000_HELPME.md)** plutôt !)

En principe, l'app doit se lancer, là, et tu dois en voir la page d'accueil...

### Si ce n'est pas le cas : Signale-le dans le [Chat LIVE](https://discord.com/channels/1056923339546968127/1507316257580519445) à minima, ou [ISSUE](https://github.com/GrCOTE7/gsm/issues/new/choose) ! Et bien-sûr, et c'est **10 000 X mieux**, si tu sais déjà le faire : **PR** (**P**ull **R**equest) pour corriger la doc tel que ce problème soit résolu ! Ne tkt pas si tu n'en es pas encore là, car que TU en soies capable au + vite est notre 1er objectif 👌.

Donc, si tout va bien, à ce stade, l'app 'tourne', et tu dois voir que la fenêtre de sortie de l'app s'actualise automatiquement dès un seul caractère du code modifié... Même si elle n'est pas forcément à un endroit optimal, selon ton matériel... Pour le moment fait la simplement glisser ailleurs qu'elle ne te gêne pas !

### 💡 Pour modifier la page d'accueil et ainsi voir que tout marche bien, dont le hot-reload: Ouvre ce fichier: gsm\src\upu\views\tests.py et modifie la ligne - elle se trouve plutôt sur la fin du script...

```python
"Page pour tests rapides.",
```

### en :

```python
"Page de MP21170 pour tests rapides.",
```

#### Et observe ta fenêtre de l'app : Se met-elle bien à jour 'toute seule' ?

( Psssiiittt: On est d'accord, tu as bien mis ton nom d'UserName GH à la place de MP21170...? )

## 🛠️ Gérons maintenant la position de la fenêtre de l'app

Aussi, considérons que tu n'as qu'un seul écran. Tu sauras adapter aisément si tu en a + 😉 !

Perso, dans un tel cas (1 seul écran dispo), je consacre 2/3 à 4/5 de la surface à l'éditeur, et le reste pour l'app. Du coup, pas besoin de toucher à rien, juste au code, et on voit direct le résultat ! En +, on a certainement une fenêtre d'app proche de la taille du rendu sur mobile, et n'oublions pas que nous seuls, codeurs, préférons encore un bon vieux PC, tous les autres sont maintenant prioritairement convertis au 'Mobile First'...

Alors, bonne nouvelle, c'est juste une valeur à indiquer dans un fichier :

1. Copie .env_example à la racine en .env
2. Pour l'heure, la seule valeur y configurer est **UPU_WINDOW_LEFT** : Elle défini où se positionnera la fenêtre de l'app sur PC... Trouve TA valeur idéale pour un positionnement aux petits oignons... (*[Encore des Oignons ?!?](../THERA.md#Philosophie---Union-DRY)*)
      Nous verrons les autres en temps utile.

📄 Pour info : Ce **fichier ./.env n'est jamais dans le Git** (Il est à toi, et rien qu'à toi, uniquement local, donc tu peux y mettre toutes infos sensibles sans inquiétude...)

---

## → 4. [On attaque **le dev** 👌 ?](./0104_GIT_DEV.md)
