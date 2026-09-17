"""Sections composant la card de diagnostic.

Chaque module expose une fonction `build() -> ft.Control | None`.
Retourner None signifie "section non disponible" (stub ou paquet absent).

`section_ui` fournit les primitives propres au diagnostic (`row`, `heading`,
`divider`) ; la gouttière de la scrollbar vient de `gsm.ui`.
"""

from . import (
    network_section,
    section_ui,
    system_section,
    versions_section,
)

__all__ = [
    "versions_section",
    "system_section",
    "network_section",
    "section_ui",
]
