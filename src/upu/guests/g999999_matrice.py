import flet as ft
from typing import Callable
from gc7_tools.helpers import sepa, sepa_outlined

from upu.guests import register

date = "29-99-99"
guest = "MATRICE POUR FUTUR TEST"
source = ""
response = ""
url = ""

from upu.views.partials.test_guests_src import guest_source

S: str = 'abc'

def vif_du_sujet():
    return f"Ici on gère le sujet..."


def subject():

    return ft.Column(
        controls=[
            guest_source(date, guest, response, source, url),
            sepa('CYAN'),
            ft.Text(vif_du_sujet(), size=20),
        ]
    )


# register(subject) # À ne décommenter que pour archiver le sujet dans REGISTRY
