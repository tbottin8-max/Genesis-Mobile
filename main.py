import flet as ft
import yfinance as yf

# Liste simplifiée et propre pour éviter tout bug de lecture
TICKERS = ["GC=F", "SI=F", "TSLA", "AAPL", "NVDA", "EURUSD=X", "GBPUSD=X", "BTC-USD"]

def analyze_logic():
    valid_candidates = []
    # On limite à une petite liste pour le premier test de stabilité
    for ticker in TICKERS:
        try:
            data = yf.download(ticker, period="2d", interval="1d", progress=False)
            if not data.empty and len(data) >= 1:
                perf = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
                if perf > 0: # On accepte tout ce qui est positif pour le test
                    valid_candidates.append({"ticker": ticker, "perf": perf})
        except:
            continue
    
    valid_candidates = sorted(valid_candidates, key=lambda x: x['perf'], reverse=True)
    gold = next((x for x in valid_candidates if "GC=F" in x['ticker']), None)
    tech = next((x for x in valid_candidates if "TSLA" in x['ticker'] or "AAPL" in x['ticker']), None)
    forex = next((x for x in valid_candidates if "=X" in x['ticker']), None)
    
    return valid_candidates, [gold, tech, forex]

def main(page: ft.Page):
    page.title = "Genesis Pilot - Stabilisé"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # Composants de l'interface
    title = ft.Text("🚀 GENESIS PILOT", size=30, weight="bold", color="gold")
    status_msg = ft.Text("Appuyez sur SCAN pour tester", color="white70")
    results = ft.Column(horizontal_alignment="center")

    def run_test(e):
        status_msg.value = "Analyse en cours..."
        results.controls.clear()
        page.update()
        
        all_v, top_3 = analyze_logic()
        
        if not all_v:
            status_msg.value = "Aucun signal détecté."
        else:
            status_msg.value = f"Succès : {len(all_v)} actifs trouvés"
            for item in top_3:
                if item:
                    results.controls.append(
                        ft.Text(f"⭐ {item['ticker']} : +{item['perf']:.2f}%", size=20)
                    )
        page.update()

    page.add(
        title,
        status_msg,
        ft.Divider(height=20, color="transparent"),
        results,
        ft.ElevatedButton("LANCER LE SCAN", on_click=run_test, width=250)
    )

ft.app(target=main)
