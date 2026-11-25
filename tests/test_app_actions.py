"""Ouverture des liens : résolution de la page et cascade de repli.

Flet 1.0 a supprimé `page.launch_url()` et expose `e.page` sur les événements
(plus de `e.control.page`). Sans ça, `open_url()` retombait sur
`webbrowser.open()`, inopérant sur Android : les liens de l'accueil ne
faisaient rien.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from upu.helpers import app_actions


class _FakePage:
    def __init__(self):
        self.tasks = []

    def run_task(self, handler, *args, **kwargs):
        self.tasks.append(handler)


class _EventWithPage:
    def __init__(self, page):
        self.page = page


class _LegacyEvent:
    def __init__(self, control):
        self.control = control


class _Control:
    def __init__(self, page):
        self.page = page


def test_as_page_reads_the_event_page():
    page = _FakePage()
    assert app_actions._as_page(_EventWithPage(page)) is page


def test_as_page_supports_legacy_control_events():
    page = _FakePage()
    assert app_actions._as_page(_LegacyEvent(_Control(page))) is page


def test_as_page_returns_none_without_a_page():
    assert app_actions._as_page(object()) is None


def test_open_url_schedules_a_launch_task_when_a_page_exists(monkeypatch):
    page = _FakePage()
    monkeypatch.setattr(app_actions, "launch_url_intent", lambda _url: False)

    app_actions.open_url(_EventWithPage(page), "https://example.com")

    assert len(page.tasks) == 1
    assert callable(page.tasks[0])


def test_open_url_falls_back_to_intent_without_a_page(monkeypatch):
    calls: list[tuple[str, str]] = []
    monkeypatch.setattr(
        app_actions,
        "launch_url_intent",
        lambda url: calls.append(("intent", url)) or True,
    )
    monkeypatch.setattr(
        app_actions.webbrowser,
        "open",
        lambda url: calls.append(("browser", url)) or True,
    )

    app_actions.open_url(object(), "https://example.com")

    assert calls == [("intent", "https://example.com")]
