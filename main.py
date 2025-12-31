import flet as ft
import yfinance as yf
import webbrowser

# Liste des 65 candidats
TICKERS = [
    "GC=F", "SI=F", "CL=F", "HG=F", "NG=F", "TSLA", "AAPL", "MSFT", "NVDA", "GOOGL",
    "EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "BTC-USD", "ETH-USD", "^GSPC", "^IXIC",
    # ... (Liste complète pour le scan)
]

def analyze_logic():
    valid_candidates = []
    for ticker in TICKERS[:65]: # Limite à 65 pour le test
        try:
            data = yf.download(ticker, period="5d", interval="1d", progress=False)
            if not data.empty and len(data) >= 2:
                perf = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
                if perf > 0.5: 
                    valid_candidates.append({"ticker": ticker, "perf": perf})
        except: continue
    
    valid_candidates = sorted(valid_candidates, key=lambda x: x['perf'], reverse=True)
    gold = next((x for x in valid_candidates if x['ticker'] in ["GC=F", "SI=F"]), None)
    tech = next((x for x in valid_candidates if x['ticker'] in ["TSLA", "NVDA", "AAPL"]), None)
    forex = next((x for x in valid_candidates if "=X" in x['ticker']), None)
    return valid_candidates, [gold, tech, forex]

def main(page: ft.Page):
    page.title = "Genesis Pilot - Sécurité Active"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = "auto"

    # --- ÉCRAN 1 : SÉCURITÉ & DISCLAIMER ---
    def accept_safety(e):
        safety_view.visible = False
        dashboard_view.visible = True
        page.update()

    safety_view = ft.Column([
        ft.Text("🛡️ CONFIGURATION DE SÉCURITÉ", size=24, weight="bold", color="gold"),
        ft.Container(
            content=ft.Text(
                "IMPORTANT : Pour garantir les rappels toutes les 30 min, "
                "vous devez autoriser l'application à ignorer l'optimisation de batterie "
                "et activer les notifications prioritaires.",
                color="white70", size=14
            ),
            padding=10, bgcolor=ft.colors.RED_900, border_radius=10
        ),
        ft.Divider(),
        ft.Text("1. Permissions Système", weight="bold"),
        ft.ElevatedButton("Raccourci Paramètres Batterie", 
            on_click=lambda _: page.launch_url("package:com.android.settings"), icon=ft.icons.BATTERY_ALERT),
        ft.Text("2. Accord de Responsabilité", weight="bold"),
        ft.Checkbox(label="Je comprends que je suis seul responsable de mes fonds.", value=False, 
            on_change=lambda e: setattr(btn_accept, "disabled", not e.control.value) or page.update()),
        ft.Divider(),
        btn_accept := ft.ElevatedButton("ACTIVER LE PILOTAGE", on_click=accept_safety, disabled=True, color="gold"),
    ], horizontal_alignment="center", visible=True)

    # --- ÉCRAN 2 : DASHBOARD (SCAN ALPHA) ---
    top_3_container = ft.Column(spacing=10)
    status_msg = ft.Text("Prêt pour l'analyse", color="grey")

    def start_scan(e):
        btn_scan.disabled = True
        status_msg.value = "Analyse des 65 candidats en cours..."
        page.update()
        
        all_v, final_3 = analyze_logic()
        
        top_3_container.controls.clear()
        if not all_v:
            status_msg.value = "🔴 ALERTE ROUGE : Aucun signal."
        else:
            status_msg.value = f"🟢 {len(all_v)} actifs en force."
            for item in final_3:
                if item:
                    top_3_container.controls.append(
                        ft.Container(
                            content=ft.Text(f"⭐ {item['ticker']} : +{item['perf']:.2f}%", size=18, weight="bold"),
                            padding=15, bgcolor=ft.colors.GREY_900, border_radius=10, border=ft.border.all(1, "gold")
                        )
                    )
        btn_scan.disabled = False
        page.update()

    btn_scan = ft.ElevatedButton("LANCER LE SCAN ALPHA", on_click=start_scan, width=300)
    
    dashboard_view = ft.Column([
        ft.Text("🚀 GENESIS DASHBOARD", size=24, weight="bold"),
        status_msg,
        top_3_container,
        ft.Divider(),
        btn_scan,
        ft.TextButton("Retour Sécurité", on_click=lambda _: setattr(safety_view, "visible", True) or setattr(dashboard_view, "visible", False) or page.update())
    ], horizontal_alignment="center", visible=False)

    page.add(ft.Center(ft.Column([safety_view, dashboard_view], horizontal_alignment="center")))

ft.app(target=main)
