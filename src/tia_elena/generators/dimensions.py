"""
Dimension tables generator.
"""
import polars as pl
import numpy as np
from pathlib import Path

from .config import REMUNERATION_CONCEPTS, SUBSIDIARIES, FX_RATES, FUNDING_FACTORS


def generate_fx_rates() -> pl.DataFrame:
    """Generate FX rates dimension table."""
    return pl.DataFrame({
        "currency": list(FX_RATES.keys()),
        "fx_rate_to_eur": list(FX_RATES.values()),
    })


def generate_mapping() -> pl.DataFrame:
    """Generate concept mapping dimension table."""
    mapping_data = []
    for concept, info in REMUNERATION_CONCEPTS.items():
        if info.get("is_variable", False):
            mapping_data.append({
                "concept_raw": concept,
                "category_normalized": info["category"],
            })
    return pl.DataFrame(mapping_data)


def generate_bonus_pool(seed: int = 456) -> pl.DataFrame:
    """Generate bonus pool allocations dimension table."""
    np.random.seed(seed)
    
    pools = []
    for sub_code, sub_info in SUBSIDIARIES.items():
        country = sub_code.split("-")[0]
        factor = FUNDING_FACTORS.get(country, 0.85)
        
        theoretical = sub_info["employees"] * 50000 * 0.15
        pool = theoretical * factor * np.random.uniform(0.9, 1.1)
        
        pools.append({
            "subsidiary_code": sub_code,
            "pool_amount_eur": round(pool, 2),
        })
    
    return pl.DataFrame(pools)


def generate_dimension_tables(data_dir: Path) -> None:
    """Generate and save all dimension tables."""
    dim_dir = data_dir / "dim"
    dim_dir.mkdir(parents=True, exist_ok=True)
    
    generate_fx_rates().write_parquet(dim_dir / "fx_rates.parquet")
    generate_mapping().write_parquet(dim_dir / "mapping.parquet")
    generate_bonus_pool().write_parquet(dim_dir / "bonus_pool.parquet")
