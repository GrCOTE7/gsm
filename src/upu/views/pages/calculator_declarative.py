from dataclasses import dataclass, field
from typing import Callable, Optional
import flet as ft
from upu.views.templates.default import named_view
from upu.helpers.app_actions import open_url
from upu.helpers.buttons import extLink

# XXX Analyse de ce code et go !

# Principales différences déclaratives :
# 1. État immuable (CalculatorState)
# L'état est un dataclass immuable

# Chaque action retourne un nouvel état au lieu de muter l'existant

# Pas de variables d'instance mutables (self.operand1, etc.)

# 2. Logique pure
# La méthode apply_input() est une fonction pure : elle prend un état et retourne un nouvel état

# Pas d'effets de bord (pas de print, pas de update() dans la logique)

# 3. Séparation claire
# Modèle : CalculatorState (état + logique)

# Vue : Composants UI (purs, sans état)

# Contrôleur : CalculatorApp (orchestre l'état et le rendu)

# 4. Rendu déclaratif
# La méthode render() met à jour l'UI à partir de l'état

# Un seul point de mise à jour (update_state())

# 5. Comparaison d'états
# On compare l'ancien et le nouvel état avant de rendre

# Permet des optimisations futures (ne rendre que ce qui a changé)

# Avantages du style déclaratif :
# ✅ Prévisibilité : L'état est toujours cohérent
# ✅ Testabilité : La logique métier est isolée et testable unitairement
# ✅ Maintenabilité : Séparation claire des responsabilités
# ✅ Débogage : Plus facile de tracer les changements d'état
# ✅ Scalabilité : Facile d'ajouter des fonctionnalités (undo/redo, persistance)

# ===== ÉTAT =====
@dataclass
class CalculatorState:
    display: str = "0"
    operand1: float = 0.0
    operator: str = "+"
    new_operand: bool = True
    error: bool = False

    def reset(self) -> "CalculatorState":
        return CalculatorState(
            display="0",
            operand1=0.0,
            operator="+",
            new_operand=True,
            error=False
        )

    def format_number(self, num: float) -> str:
        if num % 1 == 0:
            return str(int(num))
        return str(num)

    def calculate(self, operand1: float, operand2: float, operator: str) -> tuple[str, bool]:
        if operator == "+":
            return self.format_number(operand1 + operand2), False
        elif operator == "-":
            return self.format_number(operand1 - operand2), False
        elif operator == "*":
            return self.format_number(operand1 * operand2), False
        elif operator == "/":
            if operand2 == 0:
                return "Error", True
            return self.format_number(operand1 / operand2), False
        return "0", False

    def apply_input(self, data: str) -> "CalculatorState":
        # AC ou Error
        if data == "AC" or self.error:
            return self.reset()

        # Chiffres et point décimal
        if data in "0123456789.":
            if self.display == "0" or self.new_operand:
                new_display = data
            else:
                new_display = self.display + data
            return CalculatorState(
                display=new_display,
                operand1=self.operand1,
                operator=self.operator,
                new_operand=False,
                error=False
            )

        # Opérateurs (+, -, *, /)
        if data in "+-*/":
            result, error = self.calculate(self.operand1, float(self.display), self.operator)
            if error:
                return self.reset()
            return CalculatorState(
                display=result,
                operand1=float(result),
                operator=data,
                new_operand=True,
                error=False
            )

        # Égal
        if data == "=":
            result, error = self.calculate(self.operand1, float(self.display), self.operator)
            if error:
                return self.reset()
            return CalculatorState(
                display=result,
                operand1=0.0,
                operator="+",
                new_operand=True,
                error=False
            )

        # Pourcentage
        if data == "%":
            return CalculatorState(
                display=str(float(self.display) / 100),
                operand1=0.0,
                operator="+",
                new_operand=True,
                error=False
            )

        # +/- (inversion de signe)
        if data == "+/-":
            val = float(self.display)
            new_display = str(-val) if val != 0 else "0"
            return CalculatorState(
                display=new_display,
                operand1=self.operand1,
                operator=self.operator,
                new_operand=self.new_operand,
                error=False
            )

        # Backspace
        if data == "BACKSPACE":
            if self.display not in ("0", "Error") and not self.new_operand:
                new_display = self.display[:-1] or "0"
                return CalculatorState(
                    display=new_display,
                    operand1=self.operand1,
                    operator=self.operator,
                    new_operand=False,
                    error=False
                )

        return self


# ===== COMPOSANTS PURS (sans état) =====
class CalcButton(ft.Button):
    def __init__(self, content: str, on_click: Callable, expand: int = 1, **kwargs):
        super().__init__(
            content=content,
            on_click=on_click,
            expand=expand,
            style=ft.ButtonStyle(
                padding=ft.Padding(0),
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.W_600),
            ),
            **kwargs
        )


class DigitButton(CalcButton):
    def __init__(self, content: str, on_click: Callable, **kwargs):
        super().__init__(
            content=content,
            on_click=on_click,
            bgcolor=ft.Colors.WHITE_24,
            color=ft.Colors.WHITE,
            **kwargs
        )


class ActionButton(CalcButton):
    def __init__(self, content: str, on_click: Callable, **kwargs):
        super().__init__(
            content=content,
            on_click=on_click,
            bgcolor=ft.Colors.ORANGE,
            color=ft.Colors.WHITE,
            **kwargs
        )


class ExtraActionButton(CalcButton):
    def __init__(self, content: str, on_click: Callable, **kwargs):
        super().__init__(
            content=content,
            on_click=on_click,
            bgcolor=ft.Colors.BLUE_GREY_100,
            color=ft.Colors.BLACK,
            **kwargs
        )


# ===== VUE PRINCIPALE =====
class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.state = CalculatorState()
        self.width = 350
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.BorderRadius.all(20)
        self.padding = 20

        # Référence au texte du résultat pour mise à jour
        self.result_text = ft.Text(value="0", color=ft.Colors.WHITE, size=30)

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[self.result_text],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Row(controls=[
                    ExtraActionButton("AC", self.on_button_click),
                    ExtraActionButton("+/-", self.on_button_click),
                    ExtraActionButton("%", self.on_button_click),
                    ActionButton("/", self.on_button_click),
                ]),
                ft.Row(controls=[
                    DigitButton("7", self.on_button_click),
                    DigitButton("8", self.on_button_click),
                    DigitButton("9", self.on_button_click),
                    ActionButton("*", self.on_button_click),
                ]),
                ft.Row(controls=[
                    DigitButton("4", self.on_button_click),
                    DigitButton("5", self.on_button_click),
                    DigitButton("6", self.on_button_click),
                    ActionButton("-", self.on_button_click),
                ]),
                ft.Row(controls=[
                    DigitButton("1", self.on_button_click),
                    DigitButton("2", self.on_button_click),
                    DigitButton("3", self.on_button_click),
                    ActionButton("+", self.on_button_click),
                ]),
                ft.Row(controls=[
                    DigitButton("0", self.on_button_click, expand=2),
                    DigitButton(".", self.on_button_click),
                    ActionButton("=", self.on_button_click),
                ]),
            ],
            spacing=5
        )

    # ===== GESTIONNAIRES D'ÉVÉNEMENTS =====
    def on_button_click(self, e):
        data = e.control.content
        self.update_state(data)

    def on_key_pressed(self, e):
        raw_key = (e.key or "").strip()
        key_map = {
            "Enter": "=", "Numpad Enter": "=", "NumpadEnter": "=",
            "Escape": "AC", "Delete": "AC",
            "Backspace": "BACKSPACE",
            "x": "*", "X": "*",
            ",": ".", "Numpad Decimal": ".", "NumpadDecimal": ".",
            "Numpad Divide": "/", "NumpadDivide": "/",
            "Numpad Multiply": "*", "NumpadMultiply": "*",
            "Numpad Subtract": "-", "NumpadSubtract": "-",
            "Numpad Add": "+", "NumpadAdd": "+",
            "Numpad 0": "0", "Numpad0": "0",
            "Numpad 1": "1", "Numpad1": "1",
            "Numpad 2": "2", "Numpad2": "2",
            "Numpad 3": "3", "Numpad3": "3",
            "Numpad 4": "4", "Numpad4": "4",
            "Numpad 5": "5", "Numpad5": "5",
            "Numpad 6": "6", "Numpad6": "6",
            "Numpad 7": "7", "Numpad7": "7",
            "Numpad 8": "8", "Numpad8": "8",
            "Numpad 9": "9", "Numpad9": "9",
        }
        key = key_map.get(raw_key, raw_key)
        allowed = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", 
                   "+", "-", "*", "/", "=", "%", "AC", "BACKSPACE"}
        if key in allowed:
            self.update_state(key)

    # ===== MISE À JOUR D'ÉTAT DÉCLARATIVE =====
    def update_state(self, data: str):
        # Application pure de la transformation d'état
        new_state = self.state.apply_input(data)
        
        # Si l'état a changé, mettre à jour l'UI
        if new_state != self.state:
            self.state = new_state
            self.render()

    def render(self):
        """Met à jour l'UI à partir de l'état"""
        self.result_text.value = self.state.display
        self.update()


# ===== CONSTRUCTION DE L'APPLICATION =====
def build():
    calc = CalculatorApp()
    
    # Keyboard listener encapsulant la calculatrice
    keyboard_calc = ft.KeyboardListener(
        autofocus=True,
        on_key_down=calc.on_key_pressed,
        content=calc,
    )

    return named_view(
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.CALCULATE, size=32),
                ft.Text("Calculatrice Déclarative", size=28, weight=ft.FontWeight.W_600),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        "Version déclarative de la calculatrice",
        body_text_align=ft.TextAlign.CENTER,
        extra=keyboard_calc,
        bottom=extLink(
            txt='Source: Tuto doc Flet', 
            url='https://flet.dev/docs/tutorials/calculator'
        ),
    )


if __name__ == "__main__":
    ft.run(build)