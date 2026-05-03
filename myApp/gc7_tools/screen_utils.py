import flet as ft
from typing import Callable
from .constants import theme


def get_colors_theme(page: ft.Page) -> dict:
    """Retourne bg + ink selon le thème actif."""
    if page.theme_mode == ft.ThemeMode.DARK:
        return {"bg": theme["BG"], "ink": theme["FWG"]}
    return {"bg": theme["FWG"], "ink": theme["INK_DARK"]}


def apply_theme_to_texts(page: ft.Page, *texts: ft.Text) -> None:
    """Applique la couleur d'encre active à une liste de Text Flet."""
    ink = get_colors_theme(page)["ink"]
    for txt in texts:
        txt.color = ink


def make_theme_change_handler(
    page: ft.Page, texts_getter: Callable[[], list[ft.Text]]
) -> Callable[[], None]:
    """Retourne un callback qui applique les couleurs de thème aux Text fournis."""

    def _on_theme_change() -> None:
        apply_theme_to_texts(page, *texts_getter())

    return _on_theme_change


def configure_window(
    page: ft.Page,
    *,
    left: int = 1912,
    top: int = 0,
    width: int = 392,
    height: int = 1088,
) -> None:
    page.window.left = left
    page.window.top = top
    page.window.width = width
    page.window.height = height


class ZoomController:
    def __init__(
        self,
        page: ft.Page,
        content: ft.Control,
        *,
        min_scale: float = 0.7,
        max_scale: float = 3.0,
        animation_ms: int = 80,
    ):
        self.page = page
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.current_zoom = 1.0
        self.zoom_start = 1.0
        self.target = ft.Container(
            content=content,
            scale=ft.Scale(1.0, 1.0),
            animate_scale=ft.Animation(animation_ms, ft.AnimationCurve.EASE_OUT),
        )
        self.view = ft.GestureDetector(
            content=self.target,
            on_scale_start=self.on_scale_start,
            on_scale_update=self.on_scale_update,
            on_double_tap=self.on_double_tap,
        )

    def on_scale_start(self, e: ft.ScaleStartEvent) -> None:
        self.zoom_start = self.current_zoom

    def on_scale_update(self, e: ft.ScaleUpdateEvent) -> None:
        new_zoom = max(self.min_scale, min(self.max_scale, self.zoom_start * e.scale))
        if abs(new_zoom - self.current_zoom) >= 0.01:
            self.current_zoom = new_zoom
            self.target.scale = ft.Scale(self.current_zoom, self.current_zoom)
            self.page.update()

    def on_double_tap(self, e: ft.TapEvent) -> None:
        self.reset()

    def reset(self) -> None:
        self.current_zoom = 1.0
        self.zoom_start = 1.0
        self.target.scale = ft.Scale(1.0, 1.0)
        self.page.update()


def make_zoomable_view(
    page: ft.Page,
    content: ft.Control,
    *,
    min_scale: float = 0.7,
    max_scale: float = 3.0,
    animation_ms: int = 80,
) -> ft.GestureDetector:
    controller = ZoomController(
        page,
        content,
        min_scale=min_scale,
        max_scale=max_scale,
        animation_ms=animation_ms,
    )
    return controller.view


def _is_mobile_platform(page: ft.Page) -> bool:
    platform = page.platform
    if platform is None:
        return False

    is_mobile = getattr(platform, "is_mobile", None)
    if callable(is_mobile):
        return bool(is_mobile())

    platform_name = getattr(platform, "name", str(platform)).lower()
    return platform_name in {"android", "ios"}


def gc7_rules(
    page: ft.Page,
    mode: str = "DARK",
    name: str = "Ready",
    left: int = 1912,
    # left: int = 1520,  # 1912 - 392
    # width: int = 392,
    width: int = 400, # Note : 2 * 8 de marge → page.windows_width = 384
    height: int = 1088,
    defaultColors: bool = True,
) -> None:
    configure_window(page, left=left, width=width, height=height)
    page.theme_mode = ft.ThemeMode.LIGHT if mode == "LIGHT" else ft.ThemeMode.DARK
    page.title = f"GC7 - {name}"
    if defaultColors:
        page.bgcolor = "#303030" if mode == "DARK" else "#EEEEEE"

    if _is_mobile_platform(page):
        # Respecte la safe area : status bar, encoche, barre de navigation système
        m = page.media
        page.padding = ft.Padding(
            top=m.padding.top + 5,
            bottom=m.padding.bottom + 5,
            left=m.padding.left + 10,
            right=m.padding.right + 10,
        )
