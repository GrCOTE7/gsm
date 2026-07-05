from scripts.essays.salutation import cls, disclaimer, show

try:
    from rich import print
except ModuleNotFoundError:
    # Fallback pour garder le script exécutable sans dépendance optionnelle.
    from builtins import print


# uvx watchfiles "uv run python quick_test.py" .


if __name__ == "__main__":

    cls()

    disclaimer()

    show()

    print(f"\nFin de ./quick_test.py :Ambassadorship:")

    print(
        "\n( [italic]Dans la CLI, [bold blue]CTRL + Clic[/bold blue] pour ouvrir un fichier écrit en magenta.[/italic] :wink: )"
    )

    # print(locals()) # ← CTRL + / pour switch commentaire

# python.execInTerminal-icon
