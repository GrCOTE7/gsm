"""DiagnosticBlock : Card unique qui compose les sections de diagnostic."""

import flet as ft

from ...ui import ScrollArea
from .sections import network_section, system_section, versions_section
from .sections.section_ui import divider


class DiagnosticBlock:
    """Card de diagnostic de l'application."""

    MAX_HEIGHT = 500  # px — au-delà, scrollbar verticale

    # Marge intérieure de la card, posée par le Container ci-dessous.
    #
    # `RIGHT_PADDING` est le SEUL réglage de l'espace à droite de la barre de
    # scroll : la barre se pose sur le bord droit de la zone de contenu, donc
    # augmenter cette marge fait reculer la barre vers la gauche, à distance du
    # bord de la card. La mettre à 0 colle la barre au bord.
    #
    # Attention : modifier `PADDING` (gauche/haut/bas) ne déplace PAS la barre.
    # Seul `RIGHT_PADDING` agit sur elle.
    PADDING = 16  # px — côtés gauche / haut / bas
    RIGHT_PADDING = 5  # px — espace entre le bord droit et la barre de scroll

    @staticmethod
    @ft.component
    def view() -> ft.Control:
        def section(build) -> list[ft.Control]:
            """Contenu d'une section, ou liste vide si elle n'est pas dispo."""
            ctrl = build()
            return [] if ctrl is None else [ctrl]

        return ft.Card(
            content=ft.Container(
                padding=ft.Padding.only(
                    left=DiagnosticBlock.PADDING,
                    top=DiagnosticBlock.PADDING,
                    bottom=DiagnosticBlock.PADDING,
                    right=DiagnosticBlock.RIGHT_PADDING,
                ),
                # `ScrollArea.column()` fournit la scrollbar ET réserve la
                # gouttière sur chaque enfant. Les sections appliquent déjà
                # cette gouttière via `section_ui.row()` : ici on les passe
                # telles quelles, sans les ré-envelopper.
                content=ScrollArea.column(
                    height=DiagnosticBlock.MAX_HEIGHT,
                    controls=[
                        ft.Text(
                            "Diagnostic",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),
                        # Seul contrôle du bloc qui s'étend jusqu'au bord droit.
                        ScrollArea.gutter(ft.Divider(height=1)),
                        *section(versions_section.build),
                        # Séparateur entre Versions et Système (le seul inter-
                        # sections, versions_section gère déjà les siens).
                        divider(),
                        *section(system_section.build),
                        *section(network_section.build),
                    ],
                ),
            ),
        )
