import flet as ft

NAV_ITEMS = [
    {
        "route": "/home",
        "label": "Accueil",
        "icon": ft.Icons.HOME_OUTLINED,
        "selected_icon": ft.Icons.HOME,
    },
    {
        "route": "/sport",
        "label": "Sport",
        "icon": ft.Icons.SETTINGS_OUTLINED,
        "selected_icon": ft.Icons.SETTINGS,
    },
    {
        "route": "/settings",
        "label": "Parametres",
        "icon": ft.Icons.SETTINGS_OUTLINED,
        "selected_icon": ft.Icons.SETTINGS,
    }
]


def route_to_index(route: str) -> int:
    for index, item in enumerate(NAV_ITEMS):
        if item["route"] == route:
            return index
    return 0
