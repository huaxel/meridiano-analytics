"""
Input validation module.

Validates input data against schemas and business rules.
"""
import polars as pl
from typing import List

from .schemas import ValidationResult, ValidationError


def validate_remuneration_input(df: pl.DataFrame) -> ValidationResult:
    """
    Validate remuneration input data.
    
    Checks:
    - Required columns exist
    - No null values in key columns
    - Amounts are numeric
    - Currencies are valid
    
    Args:
        df: Input DataFrame to validate
        
    Returns:
        ValidationResult with errors and warnings
    """
    errors: List[ValidationError] = []
    warnings: List[str] = []
    
    required_cols = [
        "employee_id", "local_currency", "remuneration_concept", 
        "local_amount", "subsidiary_code"
    ]
    
    # Check required columns
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        for col in missing:
            errors.append(ValidationError(
                row=0, column=col, value="", 
                error=f"Required column '{col}' is missing"
            ))
        return ValidationResult(
            is_valid=False, errors=errors, warnings=warnings, 
            rows_checked=0
        )
    
    # Check null values in key columns
    null_counts = df.select([
        pl.col(c).null_count().alias(c) for c in required_cols
    ]).row(0, named=True)
    
    for col, count in null_counts.items():
        if count > 0:
            warnings.append(f"Column '{col}' has {count} null values")
    
    # Check for negative amounts (other than clawbacks)
    negative_amounts = df.filter(
        (pl.col("local_amount") < 0) & 
        (~pl.col("remuneration_concept").str.contains("(?i)clawback|malus"))
    ).height
    
    if negative_amounts > 0:
        warnings.append(f"{negative_amounts} records have unexpected negative amounts")
    
    # Check currency format issues
    non_standard_currencies = df.filter(
        pl.col("local_currency").str.len_chars() != 3
    ).height
    
    if non_standard_currencies > 0:
        warnings.append(f"{non_standard_currencies} records have non-standard currency codes")
    
    # Check for extreme amounts (potential data errors)
    extreme_amounts = df.filter(
        (pl.col("local_amount") > 1e9) | (pl.col("local_amount") < -1e9)
    ).height
    
    if extreme_amounts > 0:
        warnings.append(f"{extreme_amounts} records have extreme amounts (>1B)")
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        rows_checked=len(df)
    )


def validate_fx_rates(df: pl.DataFrame) -> ValidationResult:
    """Validate FX rates dimension table."""
    errors: List[ValidationError] = []
    warnings: List[str] = []
    
    # Check required columns
    if "currency" not in df.columns or "fx_rate_to_eur" not in df.columns:
        errors.append(ValidationError(
            row=0, column="", value="",
            error="FX rates must have 'currency' and 'fx_rate_to_eur' columns"
        ))
    
    # Check for EUR rate = 1.0
    eur_rows = df.filter(pl.col("currency") == "EUR")
    if eur_rows.height == 0:
        warnings.append("EUR rate not found in FX rates")
    elif eur_rows["fx_rate_to_eur"][0] != 1.0:
        warnings.append(f"EUR rate is {eur_rows['fx_rate_to_eur'][0]}, expected 1.0")
    
    # Check for non-positive rates
    bad_rates = df.filter(pl.col("fx_rate_to_eur") <= 0).height
    if bad_rates > 0:
        errors.append(ValidationError(
            row=0, column="fx_rate_to_eur", value="",
            error=f"{bad_rates} currencies have non-positive FX rates"
        ))
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        rows_checked=len(df)
    )
