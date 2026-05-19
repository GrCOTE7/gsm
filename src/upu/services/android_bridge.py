"""
Pont Android via pyjnius (fourni nativement par le runtime Chaquopy/serious_python).

Toutes les fonctions sont des no-ops silencieux en dehors d'Android :
les imports de jnius sont proteges par try/except, donc ce module
peut etre importe sans risque sur desktop et lors des tests.
"""

from __future__ import annotations

import logging

_log = logging.getLogger(__name__)


def launch_url_intent(url: str) -> bool:
    """Lance une URL via un Intent Android ACTION_VIEW.

    Utilise le contexte Application avec FLAG_ACTIVITY_NEW_TASK :
    pas besoin d'une reference directe a l'Activity.

    Returns:
        True si l'intent a ete envoye avec succes, False sinon.
    """
    try:
        from jnius import autoclass  # type: ignore[import-untyped]

        Intent = autoclass("android.content.Intent")
        Uri = autoclass("android.net.Uri")
        Python = autoclass("com.chaquo.python.Python")

        ctx = Python.getInstance().getApplication()
        intent = Intent(Intent.ACTION_VIEW)
        intent.setData(Uri.parse(url))
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        ctx.startActivity(intent)
        _log.info("android_bridge.launch_url_intent OK url=%s", url)
        return True
    except Exception as exc:
        _log.warning("android_bridge.launch_url_intent echec url=%s err=%s", url, exc)
        return False


def force_exit(code: int = 0) -> None:
    """Tue le process Android via java.lang.System.exit().

    Cet appel ne retourne jamais si le runtime Chaquopy est disponible.
    No-op silencieux hors Android.
    """
    try:
        from jnius import autoclass  # type: ignore[import-untyped]

        System = autoclass("java.lang.System")
        _log.info("android_bridge.force_exit code=%d", code)
        System.exit(code)
    except Exception as exc:
        _log.warning("android_bridge.force_exit echec err=%s", exc)
