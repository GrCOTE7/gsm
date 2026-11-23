"""Primitives UI réutilisables, indépendantes du métier.

Ce paquet ne connaît ni le diagnostic, ni le routage : n'importe quelle page
peut l'importer.

    from gsm.ui import ScrollArea, gutter
"""

from .scroll import GUTTER, SCROLLBAR_THICKNESS, ScrollArea, gutter

__all__ = [
    "ScrollArea",
    "gutter",
    "GUTTER",
    "SCROLLBAR_THICKNESS",
]
