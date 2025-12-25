"""
Business logic calculators.

Encapsulates the funding ratio calculation logic following the Single Responsibility Principle.
"""
import polars as pl
from .config import settings


class FundingRatioCalculator:
    """
    Calculates funding ratios based on pool budgets and demand.
    
    The funding ratio is: min(pool / demand, 1.0)
    - If demand < pool: ratio = 1.0 (full payout)
    - If demand > pool: ratio < 1.0 (proportional reduction)
    """
    
    def __init__(self, pool_df: pl.LazyFrame):
        """Initialize with bonus pool data."""
        self.pool = pool_df
    
    def calculate(self, demand_df: pl.LazyFrame) -> pl.LazyFrame:
        """
        Calculate funding ratios for each subsidiary.
        
        Args:
            demand_df: LazyFrame with 'subsidiary_code' and 'theoretical_eur' columns
            
        Returns:
            LazyFrame with subsidiary_code, pool_amount_eur, total_needed_eur, funding_ratio
        """
        # Aggregate demand by subsidiary
        subsidiary_needs = (
            demand_df
            .group_by("subsidiary_code")
            .agg(pl.col("theoretical_eur").sum().alias("total_needed_eur"))
        )
        
        # Join with pool and calculate ratio
        pool_calc = (
            self.pool
            .join(subsidiary_needs, on="subsidiary_code", how="left")
            .with_columns(
                pl.when(pl.col("total_needed_eur") > 0)
                .then(pl.col("pool_amount_eur") / pl.col("total_needed_eur"))
                .otherwise(1.0)
                .alias("funding_ratio")
            )
            .with_columns(
                pl.col("funding_ratio")
                .clip(upper_bound=settings.FUNDING_RATIO_CAP)
                .alias("funding_ratio")
            )
        )
        
        return pool_calc
