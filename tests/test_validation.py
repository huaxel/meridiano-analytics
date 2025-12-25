"""
Tests for validation module.
"""
import polars as pl
from tia_elena.validation import validate_remuneration_input, validate_fx_rates


def test_validate_valid_input():
    """Valid input should pass validation."""
    df = pl.DataFrame({
        "employee_id": ["emp1"],
        "local_currency": ["EUR"],
        "remuneration_concept": ["BONUS"],
        "local_amount": [1000.0],
        "subsidiary_code": ["ES-MAD"],
    })
    
    result = validate_remuneration_input(df)
    
    assert result.is_valid
    assert result.error_count == 0


def test_validate_missing_column():
    """Missing required column should fail."""
    df = pl.DataFrame({
        "employee_id": ["emp1"],
        # Missing local_currency, etc.
    })
    
    result = validate_remuneration_input(df)
    
    assert not result.is_valid
    assert result.error_count > 0


def test_validate_fx_rates_valid():
    """Valid FX rates should pass."""
    df = pl.DataFrame({
        "currency": ["EUR", "USD"],
        "fx_rate_to_eur": [1.0, 0.92],
    })
    
    result = validate_fx_rates(df)
    
    assert result.is_valid


def test_validate_fx_rates_negative():
    """Negative FX rate should fail."""
    df = pl.DataFrame({
        "currency": ["EUR", "USD"],
        "fx_rate_to_eur": [1.0, -0.92],
    })
    
    result = validate_fx_rates(df)
    
    assert not result.is_valid
