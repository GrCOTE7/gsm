# import qrcode
# qr = qrcode.QRCode()
# qr.add_data("http://cote7.com/gsm")
# qr.make()
# qr.print_ascii()

#  pip install qrcode[pil]


import qrcode
import flet as ft

def main(page: ft.Page):
    img = qrcode.make("http://cote7.com/gsm")
    img.save("qr.png")

    page.add(
        ft.Image(src="qr.png", width=300, height=300)
    )

ft.run(main)

