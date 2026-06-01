import flet as ft
import pyshorteners  # pip install pyshorteners

shortener = pyshorteners.Shortener()

# ❌ À finir url_shorter

class ShortLinkRow(ft.Row):
    def __init__(self, shortened_link, link_source):
        super().__init__()

        self.tooltip = link_source
        self.alignment = ft.MainAxisAlignment.CENTER

        self.controls = [
            ft.Text(shortened_link, size=16, selectable=True, italic=True),
            ft.IconButton(
                icon=ft.icons.COPY,
                on_click=lambda e: self.copy(shortened_link),
                bgcolor=ft.Colors.BLUE_700,
                tooltip="Copy",
            ),
            ft.IconButton(
                icon=ft.icons.OPEN_IN_BROWSER_OUTLINED,
                tooltip="Open in browser",
                on_click=lambda e: e.page.launch_url(shortened_link),
            ),
        ]

    def copy(self, value):
        self.page.set_clipboard(value)
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Link copied to clipboard!"),
            open=True,
        )
        self.page.update()


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "URL Shortener"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(
        title=ft.Text("URL Shortener", color=ft.Colors.WHITE),
        center_title=True,
        bgcolor=ft.Colors.BLUE,
    )

    def shorten(e):
        user_link = text_field.value

        if not user_link:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Please enter a URL in the field!"),
                open=True,
            )
            page.update()
            return

        try:
            page.add(ft.Text(f"Long URL: {user_link}", weight=ft.FontWeight.BOLD))

            page.add(
                ShortLinkRow(
                    shortened_link=shortener.tinyurl.short(user_link),
                    link_source="By tinyurl.com",
                )
            )
            page.add(
                ShortLinkRow(
                    shortened_link=shortener.chilpit.short(user_link),
                    link_source="By chilp.it",
                )
            )
            page.add(
                ShortLinkRow(
                    shortened_link=shortener.clckru.short(user_link),
                    link_source="By clck.ru",
                )
            )
            page.add(
                ShortLinkRow(
                    shortened_link=shortener.dagd.short(user_link),
                    link_source="By da.dg",
                )
            )

        except Exception as ex:
            print(ex)
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    "Sorry, an error occurred. Please retry or refresh the page."
                ),
                open=True,
            )
            page.update()

    text_field = ft.TextField(
        value="https://github.com/ndonkoHenri",
        label="Long URL",
        hint_text="Type long URL here",
        max_length=200,
        keyboard_type=ft.KeyboardType.URL,
        suffix=ft.FilledButton("Shorten!", on_click=shorten),
        on_submit=shorten,
    )

    page.add(
        text_field,
        ft.Text("Generated URLs:", weight=ft.FontWeight.BOLD, size=23),
    )


ft.app(target=main)
