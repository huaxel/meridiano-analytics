"""
Pytest configuration and fixtures.
"""
import pytest
import polars as pl


@pytest.fixture
def sample_remuneration_df() -> pl.DataFrame:
    """Small sample remuneration data for testing."""
    return pl.DataFrame({
        "employee_id": ["emp1", "emp2", "emp3"],
        "local_currency": ["USD", "EUR", "GBP"],
        "remuneration_concept": ["BONUS_ANUAL_CASH", "BONUS_ANUAL_CASH + LTIP_PERFORMANCE", "COMISION_VENTAS"],
        "local_amount": [10000.0, 20000.0, 15000.0],
        "bonus_target_pct": [0.10, 0.15, 0.20],
        "subsidiary_code": ["ES-MAD", "ES-MAD", "UK-LON"],
    })


@pytest.fixture
def sample_fx_rates_df() -> pl.DataFrame:
    """Sample FX rates for testing."""
    return pl.DataFrame({
        "currency": ["USD", "EUR", "GBP"],
        "fx_rate_to_eur": [0.92, 1.0, 1.17],
    })


@pytest.fixture
def sample_mapping_df() -> pl.DataFrame:
    """Sample concept mapping for testing."""
    return pl.DataFrame({
        "concept_raw": ["BONUS_ANUAL_CASH", "LTIP_PERFORMANCE", "COMISION_VENTAS"],
        "category_normalized": ["Bonus Anual", "LTIP Performance", "Comisiones Comerciales"],
    })


@pytest.fixture
def sample_pool_df() -> pl.DataFrame:
    """Sample bonus pool for testing."""
    return pl.DataFrame({
        "subsidiary_code": ["ES-MAD", "UK-LON"],
        "pool_amount_eur": [50000.0, 10000.0],
    })
