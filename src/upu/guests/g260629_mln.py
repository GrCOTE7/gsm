import flet as ft
from typing import Callable
from gc7_tools.helpers import sepa, sepa_outlined

from upu.guests import register

date = "26-06-29"
guest = "mln.913"
source = "Discord"
response = "GC7"
url = "https://discord.com/channels/1056923339546968127/1075041467690664070/1521157884728316076"

response = response if "response" in globals() else "En cours"  # type: ignore

from upu.views.partials.test_guests_src import guest_source

S: str = 'abc'

def jeu_abc_bac_v1():
    res = S[1::-1] + S[2]
    return f"{S = }\nS[1::-1] + S[2] => {res}"


def jeu_abc_2_bac():
    s = list(S)
    s.insert(0, s.pop(1))
    res = "".join(s)
    return f"{S = }\n''.join(...) => {res}"


def subject():

    return ft.Column(
        controls=[
            guest_source(date, guest, response, source, url),
            ft.Text(jeu_abc_bac_v1(), size=20),
            ft.Text(jeu_abc_2_bac(), size=20),
        ]
    )


register(subject)
