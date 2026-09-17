"""Sections composant la card de diagnostic.

Chaque module expose une fonction `build() -> ft.Control | None`.
Retourner None signifie "section non disponible" (stub ou paquet absent).
"""

from . import network_section, system_section, versions_section

__all__ = ["versions_section", "system_section", "network_section"]
