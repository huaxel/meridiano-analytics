"""
Data loaders following the Protocol pattern.

Provides a consistent interface for loading data from different sources (CSV, Parquet).
Uses Polars LazyFrames for optimal memory usage and query optimization.
"""
from typing import Protocol, runtime_checkable
from pathlib import Path
import polars as pl


@runtime_checkable
class DataLoader(Protocol):
    """Protocol for data loading strategies."""
    
    def load(self, path: Path) -> pl.LazyFrame:
        """Load data from the given path and return a LazyFrame."""
        ...


class ParquetLoader:
    """Load data from Parquet files."""
    
    def load(self, path: Path) -> pl.LazyFrame:
        """Scan a Parquet file into a LazyFrame."""
        if not path.exists():
            raise FileNotFoundError(f"Parquet file not found: {path}")
        return pl.scan_parquet(path)


class CsvLoader:
    """Load data from CSV files with optional schema inference."""
    
    def __init__(self, dtypes: dict[str, pl.DataType] | None = None):
        self.dtypes = dtypes
    
    def load(self, path: Path) -> pl.LazyFrame:
        """Scan a CSV file into a LazyFrame."""
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {path}")
        return pl.scan_csv(path, dtypes=self.dtypes)


class DataLoaderFactory:
    """Factory for creating appropriate loaders based on file extension."""
    
    @staticmethod
    def create(path: Path, dtypes: dict[str, pl.DataType] | None = None) -> DataLoader:
        """Create a loader based on file extension."""
        suffix = path.suffix.lower()
        
        if suffix == ".parquet":
            return ParquetLoader()
        elif suffix == ".csv":
            return CsvLoader(dtypes=dtypes)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
    
    @staticmethod
    def load(path: Path, dtypes: dict[str, pl.DataType] | None = None) -> pl.LazyFrame:
        """Convenience method to load data in one call."""
        loader = DataLoaderFactory.create(path, dtypes)
        return loader.load(path)
