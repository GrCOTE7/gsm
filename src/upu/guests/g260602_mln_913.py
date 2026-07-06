import flet as ft
from typing import Callable
from gc7_tools.helpers import sepa, sepa_outlined

from upu.guests import register

# ❌ "26-05-30 nom → Thomas - Discord", https://discord.com/channels/1056923339546968127/1075041467690664070/1510251280176517230

date='26-06-02'
guest='mlm.913'
source = "PyPro Discord"
response = 'Thomas'
url='https://discord.com/channels/1056923339546968127/1075041467690664070/1511445891062698014'

response = response if 'response' in globals() else "En cours" # type: ignore

# response=globals().get('response[0]'), 'En cours'),

# trame = "0010101011001000010010001100011000101101" # valid
trame = "0010101011001000010010001100011000101100"  # unvalid
# Réf.: https://glassus.github.io/terminale_nsi/T6_6_Epreuve_pratique/data2026/26_BCG_NSI_23/sujet.pdf)

from upu.views.partials.test_guests_src import guest_source

def is_valid_mln(trame: str) -> bool:
    compteur1 = 0
    compteur2 = 0
    compteur3 = 0
    compteur4 = 0
    for i in trame[0:8]:
        if i == "1":
            compteur1 += 1
    for j in trame[8:16]:
        if j == "1":
            compteur2 += 1
    for k in trame[16:28]:
        if k == "1":
            compteur3 += 1
    for m in trame[28:36]:
        if m == "1":
            compteur4 += 1
    if compteur1 % 2 == 1:
        parite1 = "1"
    else:
        parite1 = "0"
    if compteur2 % 2 == 1:
        parite2 = "1"
    else:
        parite2 = "0"
    if compteur3 % 2 == 1:
        parite3 = "1"
    else:
        parite3 = "0"
    if compteur4 % 2 == 1:
        parite4 = "1"
    else:
        parite4 = "0"
    if (
        parite1 == trame[36]
        and parite2 == trame[37]
        and parite3 == trame[38]
        and parite4 == trame[39]
    ):
        return True
    return False


def is_valid_thomas(trame: str) -> bool:
    bornes = [(0, 8), (8, 16), (16, 28), (28, 36)]
    for i, (debut, fin) in enumerate(bornes):
        bloc = trame[debut:fin]
        parite = "1" if bloc.count("1") % 2 == 1 else "0"
        if parite != trame[36 + i]:
            return False
    return True


def trame_validation_text(
    algo_name: str,
    trame: str,
    validator: Callable[[str], bool],
) -> ft.Text:
    return ft.Text(
        f"{algo_name} : → valide ? : {validator(trame)}",
        size=14,
        weight=ft.FontWeight.W_400,
    )


trames = [
    "0010101011001000010010001100011000101101",  # valid
    "0010101011001000010010001100011000101100",  # unvalid
]


def show_trame(id_trame=0):
    return ft.Text(trames[id_trame])


def subject():
    return ft.Column(
        [
            guest_source(date=date, guest=guest, response=response, source=source, url=url),
            
            show_trame(),
            sepa(),
            trame_validation_text("mln", trames[0], is_valid_mln),
            trame_validation_text("Thomas", trames[0], is_valid_thomas),
            sepa("YELLOW"),
            show_trame(1),
            sepa("RED_400"),
            trame_validation_text("mln", trames[1], is_valid_mln),
            trame_validation_text("Thomas", trames[1], is_valid_thomas),
        ]
    )

register(subject)
