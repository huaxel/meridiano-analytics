"""
Pure transformation functions for data processing.

All functions are stateless and take/return Polars LazyFrames.
Config values are passed as parameters for testability.
"""
import polars as pl


def explode_concepts(df: pl.LazyFrame) -> pl.LazyFrame:
    """
    Split combined remuneration concepts and distribute amounts proportionally.
    
    Input: 'BONUS_PERF + SALES_COMM' with amount 1000
    Output: Two rows, each with amount 500
    """
    return (
        df
        .with_columns(
            pl.col("remuneration_concept")
            .str.split("+")
            .alias("concepts_list")
        )
        .explode("concepts_list")
        .with_columns(
            pl.col("concepts_list").str.strip_chars().alias("concept_clean")
        )
        .with_columns(
            pl.col("concepts_list").len().over(pl.col("employee_id")).alias("num_concepts")
        )
        .with_columns(
            (pl.col("local_amount") / pl.col("num_concepts")).alias("local_amount")
        )
        .drop(["concepts_list", "num_concepts", "remuneration_concept"])
        .rename({"concept_clean": "remuneration_concept"})
    )


def enrich_with_fx(
    df: pl.LazyFrame, 
    fx_rates: pl.LazyFrame
) -> pl.LazyFrame:
    """Join with FX rates and convert local amounts to EUR."""
    return (
        df
        .join(
            fx_rates,
            left_on="local_currency",
            right_on="currency",
            how="left"
        )
        .with_columns(
            (pl.col("local_amount") * pl.col("fx_rate_to_eur")).alias("theoretical_eur")
        )
    )


def enrich_with_mapping(
    df: pl.LazyFrame,
    mapping: pl.LazyFrame,
    unmapped_value: str = "UNMAPPED"
) -> pl.LazyFrame:
    """
    Join with concept mapping to normalize categories.
    
    Args:
        df: Input DataFrame
        mapping: Mapping DataFrame with concept_raw -> category_normalized
        unmapped_value: Value to use for unmapped concepts (decoupled from config)
    """
    return (
        df
        .join(
            mapping,
            left_on="remuneration_concept",
            right_on="concept_raw",
            how="left"
        )
        .with_columns(
            pl.col("category_normalized")
            .fill_null(unmapped_value)
            .alias("category_normalized")
        )
    )


def apply_funding_ratio(
    df: pl.LazyFrame,
    pool_calc: pl.LazyFrame,
    default_ratio: float = 1.0
) -> pl.LazyFrame:
    """
    Apply funding ratio to calculate final payouts.
    
    Args:
        df: Input DataFrame with theoretical_eur
        pool_calc: Pool calculation results with funding_ratio
        default_ratio: Default ratio for missing subsidiaries (decoupled from config)
    """
    return (
        df
        .join(
            pool_calc.select(["subsidiary_code", "funding_ratio"]),
            on="subsidiary_code",
            how="left"
        )
        .with_columns(
            pl.col("funding_ratio")
            .fill_null(default_ratio)
            .alias("funding_ratio")
        )
        .with_columns(
            (pl.col("theoretical_eur") * pl.col("funding_ratio")).alias("final_payout_eur")
        )
    )


def select_output_columns(
    df: pl.LazyFrame,
    columns: list[str] | None = None
) -> pl.LazyFrame:
    """
    Select and order columns for final output.
    
    Args:
        df: Input DataFrame
        columns: Optional list of columns to select. If None, uses defaults.
    """
    default_columns = [
        "employee_id",
        "subsidiary_code",
        "job_level",
        "remuneration_concept",
        "category_normalized",
        "theoretical_eur",
        "funding_ratio",
        "final_payout_eur"
    ]
    return df.select(columns or default_columns)
