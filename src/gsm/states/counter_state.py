from dataclasses import dataclass

import flet as ft


@ft.observable
@dataclass
class CounterState:
   
    value: int = 0

    def increment(self) -> None:
        self.value += 1

    def decrement(self) -> None:
        self.value -= 1

    def set_value(self, value: int) -> None:
        self.value = value

    @property
    def is_even(self) -> bool:
        return self.value % 2 == 0