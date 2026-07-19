from dataclasses import field
from upu.views.templates.default import named_view
from upu.helpers.app_actions import open_url
from upu.helpers.buttons import extLink
import flet as ft


@ft.control
class CalcButton(ft.Button):
    expand: int = field(default_factory=lambda: 1)


@ft.control
class DigitButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.WHITE_24
    color: ft.Colors = ft.Colors.WHITE


@ft.control
class ActionButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.ORANGE
    color: ft.Colors = ft.Colors.WHITE


@ft.control
class ExtraActionButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY_100
    color: ft.Colors = ft.Colors.BLACK


@ft.control
class CalculatorApp(ft.Container):
    _counter = 0

    def init(self):
        CalculatorApp._counter += 1
        self.name = f"Calc n°{CalculatorApp._counter}"
        self.reset()
        self.width = 350
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.BorderRadius.all(20)
        self.padding = 20
        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=20)
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[self.result],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(content="AC", on_click=self.button_clicked),
                        ExtraActionButton(content="+/-", on_click=self.button_clicked),
                        ExtraActionButton(content="%", on_click=self.button_clicked),
                        ActionButton(content="/", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="7", on_click=self.button_clicked),
                        DigitButton(content="8", on_click=self.button_clicked),
                        DigitButton(content="9", on_click=self.button_clicked),
                        ActionButton(content="*", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="4", on_click=self.button_clicked),
                        DigitButton(content="5", on_click=self.button_clicked),
                        DigitButton(content="6", on_click=self.button_clicked),
                        ActionButton(content="-", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="1", on_click=self.button_clicked),
                        DigitButton(content="2", on_click=self.button_clicked),
                        DigitButton(content="3", on_click=self.button_clicked),
                        ActionButton(content="+", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            content="0", expand=2, on_click=self.button_clicked
                        ),
                        DigitButton(content=".", on_click=self.button_clicked),
                        ActionButton(content="=", on_click=self.button_clicked),
                    ]
                ),
            ]
        )

    def apply_input(self, data: str):
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data

        elif data in ("+", "-", "*", "/"):
            self.result.value = str(
                self.calculate(self.operand1, float(self.result.value), self.operator)
            )
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True

        elif data in ("="):
            self.result.value = str(
                self.calculate(self.operand1, float(self.result.value), self.operator)
            )
            print(f"→ Result = {self.result.value}")
            self.reset()

        elif data in ("%"):
            self.result.value = str(float(self.result.value) / 100)
            self.reset()

        elif data in ("+/-"):
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)

            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )

        elif data == "BACKSPACE":
            if self.result.value not in ("0", "Error") and not self.new_operand:
                self.result.value = self.result.value[:-1] or "0"

        self.update()

    def button_clicked(self, e):
        data = e.control.content
        print(f"{self.name} → Button clicked with data = {data}")
        self.apply_input(data)

    def key_pressed(self, e):
        raw_key = (e.key or "").strip()
        key_map = {
            "Enter": "=",
            "Numpad Enter": "=",
            "NumpadEnter": "=",
            "Escape": "AC",
            "Backspace": "BACKSPACE",
            "Delete": "AC",
            "x": "*",
            "X": "*",
            ",": ".",
            "Numpad Decimal": ".",
            "NumpadDecimal": ".",
            "Numpad Divide": "/",
            "NumpadDivide": "/",
            "Numpad Multiply": "*",
            "NumpadMultiply": "*",
            "Numpad Subtract": "-",
            "NumpadSubtract": "-",
            "Numpad Add": "+",
            "NumpadAdd": "+",
            "Numpad 0": "0",
            "Numpad0": "0",
            "Numpad 1": "1",
            "Numpad1": "1",
            "Numpad 2": "2",
            "Numpad2": "2",
            "Numpad 3": "3",
            "Numpad3": "3",
            "Numpad 4": "4",
            "Numpad4": "4",
            "Numpad 5": "5",
            "Numpad5": "5",
            "Numpad 6": "6",
            "Numpad6": "6",
            "Numpad 7": "7",
            "Numpad7": "7",
            "Numpad 8": "8",
            "Numpad8": "8",
            "Numpad 9": "9",
            "Numpad9": "9",
        }

        key = key_map.get(raw_key, raw_key)
        if key == raw_key:
            normalized = raw_key.lower().replace(" ", "")
            if normalized.startswith("numpad"):
                suffix = normalized.removeprefix("numpad")
                if suffix in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                    key = suffix
                elif suffix in {"add", "+"}:
                    key = "+"
                elif suffix in {"subtract", "-"}:
                    key = "-"
                elif suffix in {"multiply", "*"}:
                    key = "*"
                elif suffix in {"divide", "/"}:
                    key = "/"
                elif suffix in {"decimal", ",", "."}:
                    key = "."
                elif suffix in {"enter", "return"}:
                    key = "="
        allowed = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "+", "-", "*", "/", "=", "%", "AC", "BACKSPACE"}

        if key in allowed:
            print(f"{self.name} → Key pressed = {raw_key} mapped to {key}")
            self.apply_input(key)

    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)

        elif operator == "-":
            return self.format_number(operand1 - operand2)

        elif operator == "*":
            return self.format_number(operand1 * operand2)

        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def build():
    # page.title = "Calc App"
    # create application instance
    # calc = CalculatorApp()
    # add application's root control to the page
    # page.add(calc)

    # create application instances
    # calc2 = CalculatorApp()
    # return calc1, calc2
    # add application's root control to the page
    # page.add(calc1, calc2)
    
    # calc1 = CalculatorApp()
    # return calc1

    calc = CalculatorApp()
    keyboard_calc = ft.KeyboardListener(
        autofocus=True,
        on_key_down=calc.key_pressed,
        content=calc,
    )

    return named_view(
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.CALCULATE, size=32),
                ft.Text("Calculatrice", size=28, weight=ft.FontWeight.W_600),
            ],
            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        "\n"
        "Script de calculatrice en Python avec Flet",
        bottom=extLink(txt='Source: Tuto doc Flet', url='https://flet.dev/docs/tutorials/calculator'),
        extra=keyboard_calc,
    )

if __name__ == "__main__":

    ft.run(build) #type: ignore
