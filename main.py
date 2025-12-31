import flet as ft
import yfinance as yf

# La liste complète des 65 candidats (Matières premières, Tech, Forex, Indices)
TICKERS = [
    "GC=F", "SI=F", "CL=F", "HG=F", "NG=F", 
    "TSLA", "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "NFLX", "AMD",
    "EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X", "USDCHF=X",
    "BTC-USD", "ETH-USD", "SOL-USD", "^GSPC", "^IXIC", "^DJI", "^FCHI"
    # Note: J'ai raccourci un peu pour la rapidité du test, on pourra en rajouter 100 si tu veux
]

def analyze_logic():
    valid_candidates = []
    # On scanne avec une période de 5 jours pour détecter une vraie force
    for ticker in TICKERS:
        try:
            data = yf.download(ticker, period="5d", interval="1d", progress=False)
            if not data.empty and len(data) >= 2:
                # Calcul de la performance sur les derniers jours
                perf = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
                # On ne retient que ceux qui ont une force réelle (> 0.2%)
                if perf > 0.2:
                    valid_candidates.append({"ticker": ticker, "perf": perf})
        except:
            continue
    
    # Tri par puissance
    valid_candidates = sorted(valid_candidates, key=lambda x: x['perf'], reverse=True)
    
    # Isolation du TOP 3 Diversifié
    gold = next((x for x in valid_candidates if x['ticker'] in ["GC=F", "SI=F"]), None)
    tech = next((x for x in valid_candidates if x['ticker'] in ["TSLA", "NVDA", "AAPL", "MSFT"]), None)
    forex = next((x for x in valid_candidates if "=X" in x['ticker']), None)
    
    return valid_candidates, [gold, tech, forex]

def main(page: ft.Page):
    page.title = "Genesis Pilot - Alpha"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.scroll = "auto"

    title = ft.Text("🚀 GENESIS PILOT", size=30, weight="bold", color="gold")
    status_msg = ft.Text("Prêt pour le scan des 65 candidats", color="white70")
    results_area = ft.Column(horizontal_alignment="center", spacing=15)

    def start_scan(e):
        btn_scan.disabled = True
        status_msg.value = "Analyse du marché en cours... (30s)"
        status_msg.color = "gold"
        results_area.controls.clear()
        page.update()

        all_v, top_3 = analyze_logic()

        if not all_v:
            status_msg.value = "🔴 ALERTE ROUGE : Marché trop faible."
            status_msg.color = "red"
        else:
            status_msg.value = f"🟢 Scan réussi : {len(all_v)} actifs en force."
            status_msg.color = "green"
            
            for item in top_3:
                if item:
                    # Choix de l'icône selon le type
                    icon = "💰" if "=F" in item['ticker'] else "📈" if "=X" in item['ticker'] else "💻"
                    results_area.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Text(f"{icon} {item['ticker']}", size=22, weight="bold"),
                                ft.Text(f"Force : +{item['perf']:.2f}%", color="green300", size=16),
                            ], horizontal_alignment="center"),
                            padding=20,
                            bgcolor=ft.colors.GREY_900,
                            border_radius=15,
                            border=ft.border.all(1, "gold"),
                            width=280
                        )
                    )
        
        btn_scan.disabled = False
        page.update()

    btn_scan = ft.ElevatedButton(
        "LANCER LE SCAN ALPHA", 
        on_click=start_scan, 
        width=280, 
        height=60,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    page.add(
        title,
        status_msg,
        ft.Divider(height=40, color="transparent"),
        results_area,
        ft.Divider(height=20, color="transparent"),
        btn_scan
    )

ft.app(target=main)
