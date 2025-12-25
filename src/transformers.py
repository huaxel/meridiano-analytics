"""
Pure transformation functions for data processing.

All functions are stateless and take/return Polars LazyFrames.
This enables lazy evaluation and query optimization.
"""
import polars as pl
from .config import settings


def explode_concepts(df: pl.LazyFrame) -> pl.LazyFrame:
    """
    Split combined remuneration concepts and distribute amounts proportionally.
    
    Input: 'BONUS_PERF + SALES_COMM' with amount 1000
    Output: Two rows, each with amount 500
    """
    return (
        df
        # Split the concept string by '+'
        .with_columns(
            pl.col("remuneration_concept")
            .str.split("+")
            .alias("concepts_list")
        )
        # Explode into multiple rows
        .explode("concepts_list")
        # Clean whitespace from each concept
        .with_columns(
            pl.col("concepts_list").str.strip_chars().alias("concept_clean")
        )
        # Count how many concepts per original row (using row index)
        .with_columns(
            pl.col("concepts_list").len().over(pl.col("employee_id")).alias("num_concepts")
        )
        # Distribute amount proportionally
        .with_columns(
            (pl.col("local_amount") / pl.col("num_concepts")).alias("local_amount")
        )
        # Drop intermediate columns
        .drop(["concepts_list", "num_concepts", "remuneration_concept"])
        .rename({"concept_clean": "remuneration_concept"})
    )


def enrich_with_fx(
    df: pl.LazyFrame, 
    fx_rates: pl.LazyFrame
) -> pl.LazyFrame:
    """
    Join with FX rates and convert local amounts to EUR.
    """
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
    mapping: pl.LazyFrame
) -> pl.LazyFrame:
    """
    Join with concept mapping to normalize categories.
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
            .fill_null(settings.UNMAPPED_CATEGORY)
            .alias("category_normalized")
        )
    )


def apply_funding_ratio(
    df: pl.LazyFrame,
    pool_calc: pl.LazyFrame
) -> pl.LazyFrame:
    """
    Apply funding ratio to calculate final payouts.
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
            .fill_null(settings.DEFAULT_FUNDING_RATIO)
            .alias("funding_ratio")
        )
        .with_columns(
            (pl.col("theoretical_eur") * pl.col("funding_ratio")).alias("final_payout_eur")
        )
    )


def select_output_columns(df: pl.LazyFrame) -> pl.LazyFrame:
    """
    Select and order columns for final output.
    """
    return df.select([
        "employee_id",
        "subsidiary_code",
        "category_normalized",
        "theoretical_eur",
        "funding_ratio",
        "final_payout_eur"
    ])
