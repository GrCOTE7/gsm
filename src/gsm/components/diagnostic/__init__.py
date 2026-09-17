"""Cards de diagnostic : versions, système, réseau.

Chaque card est autonome (aucune connaissance du routage).
Le point d'entrée pour la page Test est `DiagnosticBlock`.
"""

from .diagnostic_block import DiagnosticBlock

__all__ = ["DiagnosticBlock"]
