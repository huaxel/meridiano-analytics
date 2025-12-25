"""
Tests for calculator classes.
"""
import polars as pl
from tia_elena.calculators import FundingRatioCalculator


def test_funding_ratio_underfunded(sample_pool_df):
    """Underfunded subsidiary should have ratio < 1."""
    pool = sample_pool_df.lazy()
    
    demand = pl.DataFrame({
        "subsidiary_code": ["UK-LON", "UK-LON"],
        "theoretical_eur": [15000.0, 10000.0],
    }).lazy()
    
    calculator = FundingRatioCalculator(pool)
    result = calculator.calculate(demand).collect()
    
    uk = result.filter(pl.col("subsidiary_code") == "UK-LON")
    ratio = uk["funding_ratio"][0]
    
    # 10000 / 25000 = 0.4
    assert abs(ratio - 0.4) < 0.01


def test_funding_ratio_capped_at_one(sample_pool_df):
    """Ratio should be capped at 1.0 even if pool exceeds demand."""
    pool = sample_pool_df.lazy()
    
    demand = pl.DataFrame({
        "subsidiary_code": ["ES-MAD"],
        "theoretical_eur": [10000.0],
    }).lazy()
    
    calculator = FundingRatioCalculator(pool)
    result = calculator.calculate(demand).collect()
    
    es = result.filter(pl.col("subsidiary_code") == "ES-MAD")
    ratio = es["funding_ratio"][0]
    
    assert ratio == 1.0


def test_funding_ratio_custom_cap(sample_pool_df):
    """Custom cap should be respected."""
    pool = sample_pool_df.lazy()
    
    demand = pl.DataFrame({
        "subsidiary_code": ["ES-MAD"],
        "theoretical_eur": [10000.0],
    }).lazy()
    
    calculator = FundingRatioCalculator(pool, cap=0.8)
    result = calculator.calculate(demand).collect()
    
    es = result.filter(pl.col("subsidiary_code") == "ES-MAD")
    ratio = es["funding_ratio"][0]
    
    assert ratio == 0.8
