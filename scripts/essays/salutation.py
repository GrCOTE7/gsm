try:
    from rich import print
except ModuleNotFoundError:
    # Fallback pour exécuter le script même si rich n'est pas installé.
    from builtins import print

import time
import sys

# 1fo Dans un codeSpace, faire : ' ./go w ' en CLI pour ouvrir l'App Web

# Script juste pour tester le HotReload en CodeSpace

# 1fo Change un caractère dans chaine pour tester le reload !
# 1fo  1. Le message affiché dans la console est défini dans la variable chaine

chaine = "Look bien la CLI, et change un caractère (ou +) dans la variable chaine\n(File ./scripts/essays/salutation.py)!"
nombre_de_lignes = 3  # 2do ← 2. Change ici aussi !

# 1fo  3. Ferme le hotreload avec CTRL + MAJ + C
# 2see 4. Essaie ./go dans le CLI ...aa
# 2see 5. Teste sur un script actif, les modes: F9 : RUN - F5 : Debug - F8 : hotreload


def cls(mode: bool = True) -> str:

    code = "\033c"

    # 2ar
    code = ""

    if mode:
        print(code, end="")
        return ""

    return code


def disclaimer():

    texte = "Attention, mesdames et messieurs, dans un instant, ça va commencer... Heu, non ! Vous avez déjà la main !\n"

    print(
        cls(False) + "\n[bold red]Disclaimer[/bold red] :\n"
        "Ce script est un exemple de test pour le hotreload en CodeSpace.\n"
        "Il n'a pas de fonctionnalité particulière et peut être modifié à volonté.\n"
        "Il est surtout recommandé de ne pas l'utiliser en production.\n"
    )

    for lettre in texte:
        print(lettre, end="", flush=True)
        time.sleep(0.05)
    time.sleep(1)
    # cls()


def hi():
    return chaine


def show():

    print(
        cls()
        + "\n".join(
            [
                " ".join(str(i * j) for j in range(1, i + 1))
                for i in range(1, nombre_de_lignes + 1)
            ]
            + ["", "Ready pour la suite ?", "", hi()]
        )
    )

if __name__ == "__main__":

    show()
