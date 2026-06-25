from scripts.essays.salutation import cls, show
from rich import print

import time
import sys
# uvx watchfiles "python quick_test.py" .

def disclamer():

    texte = "Attention, mesdames et messieurs, dans un instant, ça va commencer... Heu, non ! Vous avez déjà la main !"

    print(
        cls(False) + 
        "\n[bold red]Disclaimer[/bold red] :\n"
        "Ce script est un exemple de test pour le hotreload en CodeSpace.\n"
        "Il n'a pas de fonctionnalité particulière et peut être modifié à volonté.\n"
        "Il est surtout recommandé de ne pas l'utiliser en production.\n"
    )

    for lettre in texte:
        print(lettre, end="", flush=True)
        time.sleep(0.05)
    time.sleep(3)
    # cls()

if __name__ == "__main__":

    cls()


    disclamer()

    show()

    print(f'\nFin de ./quick_test.py :Ambassadorship:')

    print('\n( [italic]Dans la CLI, [bold blue]CTRL + Clic[/bold blue] pour ouvrir un fichier écrit en magenta.[/italic] :wink: )')
    
    # print(locals()) # ← CTRL + / pour switch commentaire
