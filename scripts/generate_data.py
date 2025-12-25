#!/usr/bin/env python3
"""
Generate realistic synthetic data for a global Spanish bank.

Context:
- Global Spanish bank (similar to Santander/BBVA)
- ~200,000 employees worldwide
- €60B+ revenue
- Strong presence in Spain, Latin America, UK, USA, Portugal
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import polars as pl
import numpy as np
from uuid import uuid4

from src.config import settings


# =============================================================================
# REALISTIC CONFIGURATION FOR A GLOBAL SPANISH BANK
# =============================================================================

NUM_EMPLOYEES = 200_000

# Geographic distribution (employees per region)
SUBSIDIARIES = {
    # Spain (HQ) - ~40% of employees
    "ES-MAD": {"name": "España - Madrid (HQ)", "employees": 35000, "currency": "EUR"},
    "ES-BCN": {"name": "España - Barcelona", "employees": 12000, "currency": "EUR"},
    "ES-VAL": {"name": "España - Valencia", "employees": 8000, "currency": "EUR"},
    "ES-SEV": {"name": "España - Sevilla", "employees": 6000, "currency": "EUR"},
    "ES-BIL": {"name": "España - Bilbao", "employees": 5000, "currency": "EUR"},
    
    # Latin America - ~35% of employees
    "BR-SAO": {"name": "Brasil - São Paulo", "employees": 25000, "currency": "BRL"},
    "MX-MEX": {"name": "México - CDMX", "employees": 20000, "currency": "MXN"},
    "AR-BUE": {"name": "Argentina - Buenos Aires", "employees": 8000, "currency": "ARS"},
    "CL-SCL": {"name": "Chile - Santiago", "employees": 7000, "currency": "CLP"},
    "CO-BOG": {"name": "Colombia - Bogotá", "employees": 5000, "currency": "COP"},
    "PE-LIM": {"name": "Perú - Lima", "employees": 4000, "currency": "PEN"},
    "UY-MVD": {"name": "Uruguay - Montevideo", "employees": 2000, "currency": "UYU"},
    
    # Europe & USA - ~20% of employees
    "UK-LON": {"name": "Reino Unido - Londres", "employees": 18000, "currency": "GBP"},
    "US-NYC": {"name": "USA - New York", "employees": 12000, "currency": "USD"},
    "PT-LIS": {"name": "Portugal - Lisboa", "employees": 8000, "currency": "EUR"},
    "DE-FRA": {"name": "Alemania - Frankfurt", "employees": 5000, "currency": "EUR"},
    "PL-WAR": {"name": "Polonia - Varsovia", "employees": 4000, "currency": "PLN"},
    
    # Asia - ~5% of employees
    "CN-SHA": {"name": "China - Shanghai", "employees": 3000, "currency": "CNY"},
    "SG-SIN": {"name": "Singapur", "employees": 2000, "currency": "SGD"},
    "JP-TOK": {"name": "Japón - Tokyo", "employees": 1000, "currency": "JPY"},
}

# Realistic remuneration concepts for banking
REMUNERATION_CONCEPTS = {
    # Performance bonuses (most common)
    "BONUS_ANUAL": {"weight": 0.30, "category": "Bonus Anual", "avg_pct": 0.20},
    "BONUS_TRIMESTRAL": {"weight": 0.15, "category": "Bonus Trimestral", "avg_pct": 0.05},
    
    # Deferred compensation (banking regulation: CRD IV/V)
    "DIFERIDO_3Y": {"weight": 0.12, "category": "Diferido 3 Años", "avg_pct": 0.15},
    "DIFERIDO_5Y": {"weight": 0.08, "category": "Diferido 5 Años", "avg_pct": 0.10},
    
    # Long-term incentives
    "LTIP_ACCIONES": {"weight": 0.10, "category": "LTIP Acciones", "avg_pct": 0.25},
    "PHANTOM_SHARES": {"weight": 0.05, "category": "Phantom Shares", "avg_pct": 0.15},
    
    # Sales & Commercial
    "COMISION_VENTAS": {"weight": 0.08, "category": "Comisiones Ventas", "avg_pct": 0.12},
    "INCENTIVO_CAPTACION": {"weight": 0.04, "category": "Incentivo Captación", "avg_pct": 0.08},
    
    # Retention & Special
    "RETENCION": {"weight": 0.03, "category": "Retención", "avg_pct": 0.30},
    "SIGN_ON": {"weight": 0.02, "category": "Sign-on Bonus", "avg_pct": 0.25},
    
    # Mixed (will be split)
    "BONUS_COMBINADO": {"weight": 0.03, "category": "Combinado", "avg_pct": 0.18},
}

# Job levels with salary bands (annual base in EUR)
JOB_LEVELS = {
    "L1_AUXILIAR": {"min": 18000, "max": 28000, "pct_employees": 0.15},
    "L2_GESTOR": {"min": 25000, "max": 40000, "pct_employees": 0.25},
    "L3_ESPECIALISTA": {"min": 35000, "max": 55000, "pct_employees": 0.25},
    "L4_RESPONSABLE": {"min": 50000, "max": 80000, "pct_employees": 0.15},
    "L5_GERENTE": {"min": 70000, "max": 120000, "pct_employees": 0.10},
    "L6_DIRECTOR": {"min": 100000, "max": 200000, "pct_employees": 0.06},
    "L7_DIRECTIVO": {"min": 180000, "max": 400000, "pct_employees": 0.03},
    "L8_ALTA_DIRECCION": {"min": 350000, "max": 800000, "pct_employees": 0.01},
}

# Realistic FX rates (as of Dec 2024)
FX_RATES = {
    "EUR": 1.0,
    "USD": 0.92,
    "GBP": 1.17,
    "BRL": 0.18,
    "MXN": 0.054,
    "ARS": 0.001,  # Argentina inflation
    "CLP": 0.0010,
    "COP": 0.00023,
    "PEN": 0.25,
    "UYU": 0.024,
    "PLN": 0.23,
    "CNY": 0.13,
    "SGD": 0.69,
    "JPY": 0.0063,
}


def generate_employees() -> pl.DataFrame:
    """Generate employee master data with realistic distribution."""
    print(f"Generating {NUM_EMPLOYEES:,} employees...")
    
    np.random.seed(42)
    
    employees = []
    employee_id = 0
    
    for sub_code, sub_info in SUBSIDIARIES.items():
        n = sub_info["employees"]
        
        # Generate employees for this subsidiary
        for _ in range(n):
            # Assign job level based on distribution
            level = np.random.choice(
                list(JOB_LEVELS.keys()),
                p=[JOB_LEVELS[l]["pct_employees"] for l in JOB_LEVELS]
            )
            level_info = JOB_LEVELS[level]
            
            # Generate base salary
            base_salary = np.random.uniform(level_info["min"], level_info["max"])
            
            employees.append({
                "employee_id": f"EMP{employee_id:08d}",
                "subsidiary_code": sub_code,
                "job_level": level,
                "base_salary_eur": round(base_salary, 2),
                "local_currency": sub_info["currency"],
            })
            employee_id += 1
    
    return pl.DataFrame(employees)


def generate_remuneration(employees_df: pl.DataFrame) -> pl.DataFrame:
    """Generate remuneration records based on employee data."""
    print("Generating remuneration records...")
    
    np.random.seed(123)
    
    records = []
    employees = employees_df.to_dicts()
    
    concept_list = list(REMUNERATION_CONCEPTS.keys())
    concept_weights = [REMUNERATION_CONCEPTS[c]["weight"] for c in concept_list]
    
    for emp in employees:
        # Each employee gets 1-3 remuneration concepts
        num_concepts = np.random.choice([1, 2, 3], p=[0.5, 0.35, 0.15])
        
        for _ in range(num_concepts):
            concept = np.random.choice(concept_list, p=concept_weights)
            concept_info = REMUNERATION_CONCEPTS[concept]
            
            # Calculate amount based on base salary and concept
            pct_variation = np.random.uniform(0.7, 1.3)
            amount_eur = emp["base_salary_eur"] * concept_info["avg_pct"] * pct_variation
            
            # Convert to local currency
            fx_rate = FX_RATES[emp["local_currency"]]
            local_amount = amount_eur / fx_rate if fx_rate > 0 else amount_eur
            
            # Handle combined concepts (split into two)
            if concept == "BONUS_COMBINADO":
                concept_str = "BONUS_ANUAL + LTIP_ACCIONES"
            else:
                concept_str = concept
            
            records.append({
                "employee_id": emp["employee_id"],
                "subsidiary_code": emp["subsidiary_code"],
                "local_currency": emp["local_currency"],
                "remuneration_concept": concept_str,
                "local_amount": round(local_amount, 2),
                "bonus_target_pct": round(concept_info["avg_pct"], 2),
            })
    
    return pl.DataFrame(records)


def generate_fx_rates() -> pl.DataFrame:
    """Generate FX rates table."""
    print("Generating FX rates...")
    
    return pl.DataFrame({
        "currency": list(FX_RATES.keys()),
        "fx_rate_to_eur": list(FX_RATES.values()),
    })


def generate_mapping() -> pl.DataFrame:
    """Generate concept mapping table."""
    print("Generating concept mapping...")
    
    return pl.DataFrame({
        "concept_raw": [c for c in REMUNERATION_CONCEPTS if c != "BONUS_COMBINADO"],
        "category_normalized": [
            REMUNERATION_CONCEPTS[c]["category"] 
            for c in REMUNERATION_CONCEPTS 
            if c != "BONUS_COMBINADO"
        ],
    })


def generate_bonus_pool() -> pl.DataFrame:
    """
    Generate bonus pool allocations per subsidiary.
    
    Logic: Pool = Sum of theoretical payouts * funding_factor
    Where funding_factor varies by region (some are underfunded)
    """
    print("Generating bonus pool allocations...")
    
    np.random.seed(456)
    
    # Funding factors (some regions are underfunded)
    funding_factors = {
        "ES": 0.95,  # Spain: well funded
        "BR": 0.80,  # Brazil: slightly underfunded
        "MX": 0.85,
        "AR": 0.60,  # Argentina: heavily constrained
        "CL": 0.90,
        "CO": 0.85,
        "PE": 0.80,
        "UY": 0.90,
        "UK": 0.98,  # UK: well funded
        "US": 1.00,  # USA: fully funded
        "PT": 0.92,
        "DE": 0.95,
        "PL": 0.75,
        "CN": 0.70,
        "SG": 0.95,
        "JP": 0.90,
    }
    
    pools = []
    for sub_code, sub_info in SUBSIDIARIES.items():
        country = sub_code.split("-")[0]
        factor = funding_factors.get(country, 0.85)
        
        # Estimate theoretical pool based on employees and average salary
        avg_salary = 50000  # EUR
        avg_bonus_pct = 0.15
        theoretical = sub_info["employees"] * avg_salary * avg_bonus_pct
        
        # Apply funding factor with some randomness
        pool = theoretical * factor * np.random.uniform(0.9, 1.1)
        
        pools.append({
            "subsidiary_code": sub_code,
            "pool_amount_eur": round(pool, 2),
        })
    
    return pl.DataFrame(pools)


def main():
    """Generate all realistic data files."""
    print("=" * 70)
    print("Generación de Datos - Banco Global Español")
    print("=" * 70)
    
    # Ensure directories exist
    (settings.DATA_DIR / "input").mkdir(parents=True, exist_ok=True)
    (settings.DATA_DIR / "dim").mkdir(parents=True, exist_ok=True)
    (settings.DATA_DIR / "output").mkdir(parents=True, exist_ok=True)
    
    # Generate employee base
    employees = generate_employees()
    print(f"  → {len(employees):,} empleados generados")
    
    # Generate remuneration records
    remuneration = generate_remuneration(employees)
    remuneration.write_parquet(settings.input_path)
    print(f"✓ {settings.input_path} ({len(remuneration):,} registros)")
    
    # Save employee master for reference
    employees.write_parquet(settings.DATA_DIR / "dim" / "employees.parquet")
    print(f"✓ Maestro de empleados guardado")
    
    # Dimension tables
    fx_rates = generate_fx_rates()
    fx_rates.write_parquet(settings.fx_rates_path)
    print(f"✓ {settings.fx_rates_path}")
    
    mapping = generate_mapping()
    mapping.write_parquet(settings.mapping_path)
    print(f"✓ {settings.mapping_path}")
    
    pool = generate_bonus_pool()
    pool.write_parquet(settings.bonus_pool_path)
    print(f"✓ {settings.bonus_pool_path}")
    
    # Summary stats
    print("\n" + "=" * 70)
    print("RESUMEN")
    print("=" * 70)
    total_local = remuneration["local_amount"].sum()
    print(f"  Empleados:     {len(employees):>15,}")
    print(f"  Registros:     {len(remuneration):>15,}")
    print(f"  Filiales:      {len(SUBSIDIARIES):>15}")
    print(f"  Conceptos:     {len(REMUNERATION_CONCEPTS):>15}")
    print("=" * 70)


if __name__ == "__main__":
    main()
