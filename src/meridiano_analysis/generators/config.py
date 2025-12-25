"""
Bank configuration for data generation.

Contains all the constants and configuration for realistic bank data.
"""

NUM_EMPLOYEES = 200_000

SUBSIDIARIES = {
    # Spain HQ
    "ES-MAD": {"name": "España - Madrid (HQ)", "employees": 35000, "currency": "EUR", "garbage_rate": 0.01},
    "ES-BCN": {"name": "España - Barcelona", "employees": 12000, "currency": "EUR", "garbage_rate": 0.02},
    "ES-VAL": {"name": "España - Valencia", "employees": 8000, "currency": "EUR", "garbage_rate": 0.02},
    "ES-SEV": {"name": "España - Sevilla", "employees": 6000, "currency": "EUR", "garbage_rate": 0.03},
    "ES-BIL": {"name": "España - Bilbao", "employees": 5000, "currency": "EUR", "garbage_rate": 0.02},
    
    # Latin America
    "BR-SAO": {"name": "Brasil - São Paulo", "employees": 25000, "currency": "BRL", "garbage_rate": 0.08},
    "MX-MEX": {"name": "México - CDMX", "employees": 20000, "currency": "MXN", "garbage_rate": 0.06},
    "AR-BUE": {"name": "Argentina - Buenos Aires", "employees": 8000, "currency": "ARS", "garbage_rate": 0.12},
    "CL-SCL": {"name": "Chile - Santiago", "employees": 7000, "currency": "CLP", "garbage_rate": 0.05},
    "CO-BOG": {"name": "Colombia - Bogotá", "employees": 5000, "currency": "COP", "garbage_rate": 0.07},
    "PE-LIM": {"name": "Perú - Lima", "employees": 4000, "currency": "PEN", "garbage_rate": 0.09},
    "UY-MVD": {"name": "Uruguay - Montevideo", "employees": 2000, "currency": "UYU", "garbage_rate": 0.04},
    
    # Europe & USA
    "UK-LON": {"name": "Reino Unido - Londres", "employees": 18000, "currency": "GBP", "garbage_rate": 0.02},
    "US-NYC": {"name": "USA - New York", "employees": 12000, "currency": "USD", "garbage_rate": 0.01},
    "PT-LIS": {"name": "Portugal - Lisboa", "employees": 8000, "currency": "EUR", "garbage_rate": 0.03},
    "DE-FRA": {"name": "Alemania - Frankfurt", "employees": 5000, "currency": "EUR", "garbage_rate": 0.01},
    "PL-WAR": {"name": "Polonia - Varsovia", "employees": 4000, "currency": "PLN", "garbage_rate": 0.05},
    
    # Asia
    "CN-SHA": {"name": "China - Shanghai", "employees": 3000, "currency": "CNY", "garbage_rate": 0.10},
    "SG-SIN": {"name": "Singapur", "employees": 2000, "currency": "SGD", "garbage_rate": 0.03},
    "JP-TOK": {"name": "Japón - Tokyo", "employees": 1000, "currency": "JPY", "garbage_rate": 0.04},
}

REMUNERATION_CONCEPTS = {
    "BONUS_ANUAL_CASH": {"category": "Bonus Anual", "weight": 0.20, "avg_pct": 0.25, "is_variable": True},
    "BONUS_DISCRECIONAL": {"category": "Bonus Discrecional", "weight": 0.08, "avg_pct": 0.15, "is_variable": True},
    "DIFERIDO_3Y_CASH": {"category": "Diferido Cash 3Y", "weight": 0.12, "avg_pct": 0.12, "is_variable": True, "is_deferred": True},
    "DIFERIDO_5Y_CASH": {"category": "Diferido Cash 5Y", "weight": 0.06, "avg_pct": 0.08, "is_variable": True, "is_deferred": True},
    "DIFERIDO_3Y_ACCIONES": {"category": "Diferido Acciones 3Y", "weight": 0.10, "avg_pct": 0.15, "is_variable": True, "is_deferred": True, "is_equity": True},
    "DIFERIDO_5Y_ACCIONES": {"category": "Diferido Acciones 5Y", "weight": 0.05, "avg_pct": 0.10, "is_variable": True, "is_deferred": True, "is_equity": True},
    "LTIP_PERFORMANCE": {"category": "LTIP Performance", "weight": 0.08, "avg_pct": 0.20, "is_variable": True, "is_deferred": True, "is_equity": True},
    "PSU_PLAN": {"category": "Performance Share Units", "weight": 0.05, "avg_pct": 0.18, "is_variable": True, "is_deferred": True, "is_equity": True},
    "PHANTOM_SHARES": {"category": "Phantom Shares", "weight": 0.04, "avg_pct": 0.12, "is_variable": True, "is_deferred": True},
    "COMISION_VENTAS": {"category": "Comisiones Comerciales", "weight": 0.06, "avg_pct": 0.10, "is_variable": True},
    "INCENTIVO_CAPTACION": {"category": "Incentivo Captación", "weight": 0.03, "avg_pct": 0.08, "is_variable": True},
    "RETENCION": {"category": "Retención", "weight": 0.02, "avg_pct": 0.30, "is_variable": True},
    "SIGN_ON_BONUS": {"category": "Sign-on Bonus", "weight": 0.01, "avg_pct": 0.25, "is_variable": True},
    "SEVERANCE": {"category": "Indemnización", "weight": 0.01, "avg_pct": 0.50, "is_variable": True},
    "CLAWBACK": {"category": "Clawback", "weight": 0.005, "avg_pct": -0.20, "is_variable": True, "is_adjustment": True},
    "MALUS": {"category": "Malus", "weight": 0.005, "avg_pct": -0.15, "is_variable": True, "is_adjustment": True},
}

JOB_LEVELS = {
    "L1_AUXILIAR": {"min": 18000, "max": 28000, "pct": 0.15, "mrt_eligible": False},
    "L2_GESTOR": {"min": 25000, "max": 40000, "pct": 0.25, "mrt_eligible": False},
    "L3_ESPECIALISTA": {"min": 35000, "max": 55000, "pct": 0.20, "mrt_eligible": False},
    "L4_RESPONSABLE": {"min": 50000, "max": 80000, "pct": 0.15, "mrt_eligible": False},
    "L5_GERENTE": {"min": 70000, "max": 120000, "pct": 0.12, "mrt_eligible": True},
    "L6_DIRECTOR": {"min": 100000, "max": 200000, "pct": 0.08, "mrt_eligible": True},
    "L7_DIRECTIVO": {"min": 180000, "max": 400000, "pct": 0.04, "mrt_eligible": True},
    "L8_COMITE_DIRECCION": {"min": 350000, "max": 800000, "pct": 0.009, "mrt_eligible": True},
    "L9_C_SUITE": {"min": 700000, "max": 2500000, "pct": 0.001, "mrt_eligible": True},
}

FX_RATES = {
    "EUR": 1.0, "USD": 0.92, "GBP": 1.17, "BRL": 0.18, "MXN": 0.054,
    "ARS": 0.001, "CLP": 0.0010, "COP": 0.00023, "PEN": 0.25, "UYU": 0.024,
    "PLN": 0.23, "CNY": 0.13, "SGD": 0.69, "JPY": 0.0063,
}

FUNDING_FACTORS = {
    "ES": 0.95, "UK": 0.98, "US": 1.0, "DE": 0.95, "PT": 0.92,
    "BR": 0.80, "MX": 0.85, "AR": 0.60, "CL": 0.90, "CO": 0.85,
    "PE": 0.80, "UY": 0.90, "PL": 0.75, "CN": 0.70, "SG": 0.95, "JP": 0.90
}
