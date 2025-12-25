#!/usr/bin/env python3
"""
Run the ETL pipeline.

Usage:
    python scripts/run_etl.py
    python scripts/run_etl.py --export-csv
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse

from src.pipeline import run_pipeline
from src.config import settings
from src.exporters import CsvExporter


def main():
    parser = argparse.ArgumentParser(description="Run the remuneration ETL pipeline")
    parser.add_argument(
        "--export-csv",
        action="store_true",
        help="Also export results to CSV for external tools",
    )
    args = parser.parse_args()
    
    print("=" * 60)
    print("Remuneration ETL Pipeline")
    print("=" * 60)
    
    result = run_pipeline()
    
    print(f"\n✓ Output: {result.output_path}")
    print(f"✓ Audit:  {result.audit_path}")
    print(f"✓ Rows:   {result.rows_processed:,}")
    print(f"✓ Time:   {result.execution_time_seconds:.2f}s")
    
    if args.export_csv:
        import polars as pl
        
        csv_path = settings.DATA_DIR / settings.OUTPUT_CSV_EXPORT
        df = pl.read_parquet(result.output_path)
        CsvExporter().export(df, csv_path)
        print(f"✓ CSV Export: {csv_path}")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
