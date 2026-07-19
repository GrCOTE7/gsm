import flet as ft
from typing import Callable
from gc7_tools.helpers import sepa, sepa_outlined

from upu.guests import register

date = "26-07-99"
guest = "Sujet XXX"
source = "NNN Discord"
response = ""
url = ""

from upu.views.partials.test_guests_src import guest_source

S: str = 'abc'

def vif_du_sujet():
    return f"Le sujet..."

def clicked_btn(msg='') -> ft.Text:
    return ft.Text(f'Cliqued ? {msg}')

def essai(target: ft.Text):

    def button_click(e):
        target.value = "Cliqued ? Oui !"
        target.update()

    return ft.Button("Click me", on_click=button_click)

def subject():

    clicked_status = clicked_btn()

    return ft.Column(
        controls=[
            guest_source(date, guest, response, source, url),
            sepa('CYAN'),
            ft.Text(vif_du_sujet(), size=20),
            sepa('CYAN'),
            clicked_status,
            essai(clicked_status),
        ]
    )


# register(subject) # À ne décommenter que pour archiver le sujet dans REGISTRY
