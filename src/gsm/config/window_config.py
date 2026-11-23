from dataclasses import dataclass, field
import flet as ft


from ..helpers.env import get_env, curr_time

sl = "-" * 54


@dataclass
class WindowConfig:
    """Position de la fenêtre de l'application sur l'écran, ainsi que sa taille et son comportement.
    1 - 1386 x 1038 (D)
    2 - 810 x 1412 pour vidéo - Capture: ←2 ↑3 ↔1386 ↕800
    3 - 1913 x 1080 (Écran 2 - Pos 1)  ← aligné sur UPU (2ᵉ écran sans barre des tâches)
    3 - 2475 x 1080 (  "     - Pos 2)
    """

    top: int = 0
    left: int = int(
        str(get_env("GSM_WINDOW_LEFT", "856"))  # D: 1386 - 1913 - 2475 - 840 (vidéo)
    )
    width: int = 540  # 540 → 524 net interne)
    height: int = 1038

    need_cli_below: int = int(
        get_env("GSM_WINDOW_CLI", "0")  # Si absent dans .env, défaut avec le 1er 0 ou 1
        or "0"
    )  # 0 ('défaut) pas de CLI sous la fenêtre - 1 → 300 px de place dessous pour la CLI
    # print(sl + f"\n{dv(left)} | {dv(width)} | {dv(height)}" + sl)
    # print(sl+f"{need_cli_below = } (window.py)\n" + sl)
    
    resizable: bool = True

    def __post_init__(self):
        if self.left > 1912:
            # 1080 = hauteur exacte du 2ᵉ écran (1920×1080, pas de barre des
            # tâches) → alignée sur la fenêtre UPU (gc7_rules).
            self.height = 1080

    def apply(self, page: ft.Page):
        if self.left < 1373:
            print("Focus à l'App !")
            self.height = 825
            # page.run_task(page.window.to_front)  # ← Pour donner le focus à l'App

        # print(f"{self.need_cli_below = } (window.py)" + sl)

        page.window.width = self.width

        # -301 : hauteur CLI dédiée = 1080 - 301 = 779 px (identique à l'ancien
        # 1086 - 307), pour que la CLI (posée à top=779 par place_cli_window)
        # reste exactement collée sous l'app.
        self.height = self.height - 301 if self.need_cli_below else self.height
        # page.window.height = h

        page.window.top = self.top
        page.window.left = self.left
        page.window.height = self.height

        page.window.resizable = self.resizable

        # print(
        #     self.sl
        #     + f"\nleft = {self.left} | width = {self.width} | height = {self.height} | need_cli_below = {self.need_cli_below}"
        #     + self.sl
        # )

        # import inspect
        # print(inspect.iscoroutinefunction(ft.Window.to_front))
        # print(inspect.signature(ft.Window.to_front))

        print(
            {
                "écran": 1 if self.left <= 1386 else 2,
                "top": int(page.window.top),
                "left": page.window.left,
                "width": int(page.window.width),
                "height": page.window.height,
                "need_cli": self.need_cli_below,
            }
        )

        print(f"{curr_time()}", end=" > ")
        # page.theme_mode = ft.ThemeMode.LIGHT
        # page.theme_mode = ft.ThemeMode.DARK
        page.update()
