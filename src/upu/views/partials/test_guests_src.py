import flet as ft
import rich

def guest_source(
    date="Date inconnue",
    guest="Auteur inconnu",
    response="Pas encore",
    source="Source inconnue",
    url="",
):

    response_aff = f" → {response}" if response else ""

    # Construction du TextSpan avec url seulement si non vide
    span_kwargs = {
        "text": f"{date} | {guest}{response_aff} - {source}",
        "style": ft.TextStyle(
            size=16,
            color=ft.Colors.BLUE,
        ),
    }

    if url:
        span_kwargs["url"] = url

    return ft.Text(
        spans=[ft.TextSpan(**span_kwargs)],
        tooltip="Voir le msg source originel" if url else None
    )
