"""Primitives de présentation propres aux sections de diagnostic.

Les briques réellement génériques (gouttière, zone défilante) vivent dans
`gsm.ui` : ce module ne contient que ce qui a un sens *pour un diagnostic* —
une ligne « libellé / valeur » et un titre de section.

`row()` applique la gouttière de la scrollbar par construction. Une section ne
doit donc **pas** être ré-enveloppée dans `gutter()`, ni passée à
`ScrollArea.column()` : ce serait 2 x `GUTTER` de marge.
"""

import flet as ft

from ....ui import gutter


def row(label: str, value: str) -> ft.Control:
    """Ligne « libellé à gauche / valeur à droite », à l'épreuve de la scrollbar.

    La valeur est `selectable` (versions, chemins, PID… se copient). L'appel à
    `gutter()` est intégré : ne pas ré-envelopper le résultat.

    Args:
        label: Texte du libellé.
        value: Texte de la valeur, aligné à droite.

    Returns:
        Un `Row` enveloppé dans la gouttière.
    """
    return gutter(
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(label, weight=ft.FontWeight.W_500),
                ft.Text(value, selectable=True),
            ],
        )
    )


def heading(text: str) -> ft.Control:
    """Titre de section (gras italique).

    Pas de gouttière : le texte est aligné à gauche, donc jamais sous la
    scrollbar.
    """
    return ft.Text(text, size=14, weight=ft.FontWeight.BOLD, italic=True)


def divider(height: int = 8) -> ft.Control:
    """Séparateur qui s'arrête au bord des valeurs, gouttière comprise."""
    return gutter(ft.Divider(height=height))
