"""DiagnosticBlock : Card unique qui compose les sections de diagnostic.

Chaque section retourne un ft.Control ou None. Les sections vides sont
automatiquement exclues de la card finale — donc les stubs futurs
(system, network) n'apparaissent pas tant qu'ils ne sont pas implémentés.
"""

import flet as ft

from .sections import network_section, system_section, versions_section


class DiagnosticBlock:
    """Card de diagnostic de l'application."""

    @staticmethod
    @ft.component
    def view() -> ft.Control:
        section_builders = (
            versions_section.build,
            system_section.build,
            network_section.build,
        )

        rendered = [ctrl for build in section_builders if (ctrl := build()) is not None]

        return ft.Card(
            content=ft.Container(
                padding=16,
                content=ft.Column(
                    spacing=16,
                    controls=[
                        ft.Text(
                            "Diagnostic",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Divider(height=1),
                        *rendered,
                    ],
                ),
            ),
        )
