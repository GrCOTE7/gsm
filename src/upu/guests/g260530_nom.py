import flet as ft
from typing import Callable
from gc7_tools.helpers import sepa, sepa_outlined

from upu.guests import register

date = "26-05-30"
guest = "nom"
source = "PyPro Discord"
response = "Thomas"
url = "https://discord.com/channels/1056923339546968127/1075041467690664070/1510251280176517230"

response = response if "response" in globals() else "En cours"  # type: ignore

from upu.views.partials.test_guests_src import guest_source


def subject():
    rep = "\n".join(" ".join(str(i * j) for j in range(1, i + 1)) for i in range(1, 6))
    return ft.Column(
        controls=[
            guest_source(date, guest, response, source, url),
            ft.Text(rep, size=20)
        ]
    )


register(subject)