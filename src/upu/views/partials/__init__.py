"""Partials de la vue UPU (ancienne app, conservée pour mémoire)."""

import os

from .release_update_card import build_release_update_card


def build_release_update_card_if_relevant(width: int = 360):
    """Carte « nouvelle version disponible », sauf quand UPU tourne seule.

    UPU_ALONE=1 est posé par le launcher en mode `./go u` : UPU y est la
    version conservée pour mémoire, donc proposer une mise à jour n'a pas de
    sens. La carte reste affichée en `./go gu`, où UPU est vraiment utilisée.
    """
    if os.getenv("UPU_ALONE") == "1":
        return None
    return build_release_update_card(width)


__all__ = [
    "build_release_update_card",
    "build_release_update_card_if_relevant",
]
