import flet as ft

def guest_source():
    return ft.Text(
            spans=[
                ft.TextSpan(
                    # "26-05-30 nom → Thomas - Discord", https://discord.com/channels/1056923339546968127/1075041467690664070/1510251280176517230
                    "26-06-02 mlm.913 → Thomas - Discord",
                    url="https://discord.com/channels/1056923339546968127/1075041467690664070/1511445891062698014",
                    style=ft.TextStyle(
                        size=18,
                        # weight=ft.FontWeight.W_400,
                        color=ft.Colors.BLUE,
                        # decoration=ft.TextDecoration.UNDERLINE,
                    ),
                ),
            ],
            tooltip='Voir le msg source originel'
        )