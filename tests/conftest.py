from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
import sys
from typing import Callable

import flet as ft
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from upu.views.pages.registry import get_view_builder, has_route

# uv run pytest -q # -q + silencieux | -dd encore + silencieux | -v + verbeux
# uv run pytest -s -o log_cli=true -o log_cli_level=DEBUG

def _iter_controls(control: ft.Control):
    stack = [control]
    while stack:
        current = stack.pop()
        yield current

        children = []
        controls = getattr(current, "controls", None)
        if controls:
            children.extend(controls)

        content = getattr(current, "content", None)
        if isinstance(content, ft.Control):
            children.append(content)

        stack.extend(reversed(children))


@dataclass
class _Finder:
    matches: list[ft.Control]
    index: int = 0

    @property
    def count(self) -> int:
        return len(self.matches)


class _Tester:
    def __init__(self, root: ft.Control):
        self._root = root

    def pump_and_settle(self):
        return None

    def find_by_text(self, text: str) -> _Finder:
        matches: list[ft.Control] = []
        for ctrl in _iter_controls(self._root):
            if isinstance(ctrl, ft.Text) and str(ctrl.value) == text:
                matches.append(ctrl)
        return _Finder(matches=matches)

    def find_by_text_containing(self, text: str) -> _Finder:
        matches: list[ft.Control] = []
        for ctrl in _iter_controls(self._root):
            if isinstance(ctrl, ft.Text) and text in str(ctrl.value):
                matches.append(ctrl)
        return _Finder(matches=matches)

    def find_by_key(self, key: str) -> _Finder:
        matches: list[ft.Control] = []
        for ctrl in _iter_controls(self._root):
            if str(getattr(ctrl, "key", "")) == key:
                matches.append(ctrl)
        return _Finder(matches=matches)

    def tap(self, finder: _Finder):
        if finder.count == 0:
            raise AssertionError("No control found for tap")

        control = finder.matches[finder.index]
        on_click = getattr(control, "on_click", None)
        if not callable(on_click):
            raise AssertionError("Found control is not clickable")

        page = None
        try:
            page = control.page
        except RuntimeError:
            page = None

        on_click(SimpleNamespace(control=control, page=page))


@pytest.fixture
def flet_app_factory() -> Callable[[str], SimpleNamespace]:
    def _build(route: str = "/counter") -> SimpleNamespace:
        if not has_route(route):
            raise AssertionError(f"Unknown app route for test: {route}")

        root = get_view_builder(route)()
        return SimpleNamespace(route=route, tester=_Tester(root))

    return _build


@pytest.fixture
def flet_app(request: pytest.FixtureRequest, flet_app_factory: Callable[[str], SimpleNamespace]):
    route = getattr(request, "param", "/counter")
    if not isinstance(route, str):
        raise AssertionError("Fixture 'flet_app' expects a string route, e.g. '/counter'")
    return flet_app_factory(route)