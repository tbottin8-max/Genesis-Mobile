import flet as ft
import yfinance as yf

def main(page: ft.Page):
    page.title = "Genesis Mobile"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    txt_status = ft.Text("Appuyez pour scanner l'Or", size=20)
    
    def check_price(e):
        txt_status.value = "Connexion..."
        page.update()
        try:
            data = yf.download("GC=F", period="1d", progress=False)
            if len(data) > 0:
                price = data['Close'].iloc[-1]
                valeur = float(price)
                txt_status.value = f"Prix Or : ${valeur:.2f}"
                txt_status.color = "green"
            else:
                txt_status.value = "Pas de données (Marché fermé?)"
        except:
            txt_status.value = "Erreur réseau"
        page.update()

    page.add(
        ft.Column(
            [
                ft.Text("🚀 GENESIS PILOT", size=30, weight="bold"),
                txt_status,
                ft.ElevatedButton("SCANNER", on_click=check_price),
            ],
            alignment="center",
            horizontal_alignment="center"
        )
    )

ft.app(target=main)
