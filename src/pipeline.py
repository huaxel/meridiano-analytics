"""
ETL Pipeline orchestrator.

Coordinates the full ETL process using dependency injection for flexibility and testability.
"""
import time
import logging
from pathlib import Path
from dataclasses import dataclass

import polars as pl

from .config import settings
from .loaders import DataLoaderFactory
from .transformers import (
    explode_concepts,
    enrich_with_fx,
    enrich_with_mapping,
    apply_funding_ratio,
    select_output_columns,
)
from .calculators import FundingRatioCalculator
from .exporters import DataExporterFactory


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    """Result of an ETL pipeline run."""
    
    output_path: Path
    audit_path: Path
    rows_processed: int
    execution_time_seconds: float


class ETLPipeline:
    """
    Orchestrates the full ETL process for remuneration data.
    
    Uses dependency injection for loaders and exporters, making it
    easy to test and extend.
    """
    
    def __init__(
        self,
        input_path: Path | None = None,
        fx_path: Path | None = None,
        mapping_path: Path | None = None,
        pool_path: Path | None = None,
        output_path: Path | None = None,
        audit_path: Path | None = None,
    ):
        """Initialize with optional custom paths."""
        self.input_path = input_path or settings.input_path
        self.fx_path = fx_path or settings.fx_rates_path
        self.mapping_path = mapping_path or settings.mapping_path
        self.pool_path = pool_path or settings.bonus_pool_path
        self.output_path = output_path or settings.output_path
        self.audit_path = audit_path or settings.audit_path
    
    def run(self) -> PipelineResult:
        """
        Execute the full ETL pipeline.
        
        Returns:
            PipelineResult with output paths and metrics.
        """
        start_time = time.time()
        logger.info("Starting ETL Pipeline")
        
        # 1. Load data
        logger.info("Loading input data...")
        df_main = DataLoaderFactory.load(self.input_path)
        df_fx = DataLoaderFactory.load(self.fx_path)
        df_mapping = DataLoaderFactory.load(self.mapping_path)
        df_pool = DataLoaderFactory.load(self.pool_path)
        
        # 2. Transform: explode concepts
        logger.info("Transforming: exploding combined concepts...")
        df_exploded = explode_concepts(df_main)
        
        # 3. Enrich: FX rates and mapping
        logger.info("Enriching: applying FX rates and category mapping...")
        df_enriched = enrich_with_fx(df_exploded, df_fx)
        df_enriched = enrich_with_mapping(df_enriched, df_mapping)
        
        # 4. Calculate: funding ratios
        logger.info("Calculating: funding ratios by subsidiary...")
        calculator = FundingRatioCalculator(df_pool)
        pool_calc = calculator.calculate(df_enriched)
        
        # 5. Apply funding ratio and select output columns
        logger.info("Applying: funding ratios to payouts...")
        df_final = apply_funding_ratio(df_enriched, pool_calc)
        df_output = select_output_columns(df_final)
        
        # 6. Collect (execute lazy query)
        logger.info("Collecting: executing lazy query...")
        df_output_collected = df_output.collect()
        pool_calc_collected = pool_calc.collect()
        
        # 7. Export results
        logger.info(f"Exporting: {len(df_output_collected)} rows to {self.output_path}")
        DataExporterFactory.export(df_output_collected, self.output_path)
        DataExporterFactory.export(pool_calc_collected, self.audit_path)
        
        elapsed = time.time() - start_time
        logger.info(f"Pipeline completed in {elapsed:.2f} seconds")
        
        return PipelineResult(
            output_path=self.output_path,
            audit_path=self.audit_path,
            rows_processed=len(df_output_collected),
            execution_time_seconds=elapsed,
        )


def run_pipeline() -> PipelineResult:
    """Convenience function to run the default pipeline."""
    pipeline = ETLPipeline()
    return pipeline.run()


if __name__ == "__main__":
    result = run_pipeline()
    print(f"✓ Processed {result.rows_processed} rows in {result.execution_time_seconds:.2f}s")
