"""
Centralized theme configuration for the dashboard.
"""

COLORS = {
    "primary": "#C41E3A",
    "secondary": "#8B0000",
    "accent": "#E31837",
    "highlight": "#FF4D4D",
    "neutral": "#4a4a5a",
    "background": "#0F1419",
    "surface": "#1A1F26",
    "text": "#FFFFFF",
    "text_muted": "#B0B0B0",
    "success": "#00A86B",
    "warning": "#FFB800",
}

CHART_COLORS = [
    "#C41E3A", "#E31837", "#FF4D4D", "#FF8080",
    "#FFB3B3", "#2E86AB", "#A23B72", "#F18F01"
]

PAGE_CSS = """
<style>
.stApp { background: linear-gradient(180deg, #0F1419 0%, #1A1F26 100%); }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #1A1F26 0%, #0F1419 100%); border-right: 2px solid #C41E3A; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label { color: #ffffff !important; }
.main-header { background: linear-gradient(135deg, #C41E3A 0%, #8B0000 50%, #C41E3A 100%); padding: 1.5rem 2rem; border-radius: 0 0 20px 20px; margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(196, 30, 58, 0.3); border-bottom: 3px solid #FFD700; }
.main-header h1 { color: #ffffff; font-family: 'Georgia', serif; font-weight: 700; margin: 0; font-size: 1.8rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
.main-header p { color: rgba(255, 255, 255, 0.9); margin: 0.5rem 0 0 0; font-size: 0.95rem; }
[data-testid="stMetric"] { background: linear-gradient(145deg, #1A1F26 0%, #252D38 100%); border: 1px solid rgba(196, 30, 58, 0.5); border-radius: 12px; padding: 1.2rem; box-shadow: 0 4px 20px rgba(196, 30, 58, 0.15); }
[data-testid="stMetricLabel"] { color: #B0B0B0 !important; font-weight: 600; font-size: 0.85rem !important; }
[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 1.6rem !important; font-weight: 700 !important; }
.stSubheader, h3 { color: #ffffff !important; border-bottom: 2px solid #C41E3A; padding-bottom: 0.5rem; font-weight: 600; }
hr { border-color: rgba(196, 30, 58, 0.4) !important; }
</style>
"""

HEADER_HTML = """
<div class="main-header">
    <h1>🏦 Banco Meridiano | Panel de Retribución</h1>
    <p>Área de Personas & Cultura · Visión Ejecutiva Global</p>
    <p style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.8;">Reporte: Doña Submarino Invisible 🕵️‍♀️</p>
</div>
"""


SUBSIDIARY_NAMES = {
    "ES-MAD": "🇪🇸 España - Madrid (HQ)", "ES-BCN": "🇪🇸 España - Barcelona",
    "ES-VAL": "🇪🇸 España - Valencia", "ES-SEV": "🇪🇸 España - Sevilla",
    "ES-BIL": "🇪🇸 España - Bilbao", "BR-SAO": "🇧🇷 Brasil - São Paulo",
    "MX-MEX": "🇲🇽 México - CDMX", "AR-BUE": "🇦🇷 Argentina - Buenos Aires",
    "CL-SCL": "🇨🇱 Chile - Santiago", "CO-BOG": "🇨🇴 Colombia - Bogotá",
    "PE-LIM": "🇵🇪 Perú - Lima", "UY-MVD": "🇺🇾 Uruguay - Montevideo",
    "UK-LON": "🇬🇧 Reino Unido - Londres", "US-NYC": "🇺🇸 USA - New York",
    "PT-LIS": "🇵🇹 Portugal - Lisboa", "DE-FRA": "🇩🇪 Alemania - Frankfurt",
    "PL-WAR": "🇵🇱 Polonia - Varsovia", "CN-SHA": "🇨🇳 China - Shanghai",
    "SG-SIN": "🇸🇬 Singapur", "JP-TOK": "🇯🇵 Japón - Tokyo",
}
