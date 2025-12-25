"""
Data exporters following the Protocol pattern.

Provides a consistent interface for writing data to different formats.
"""
from typing import Protocol, runtime_checkable
from pathlib import Path
import polars as pl


@runtime_checkable
class DataExporter(Protocol):
    """Protocol for data export strategies."""
    
    def export(self, df: pl.DataFrame, path: Path) -> None:
        """Export DataFrame to the given path."""
        ...


class ParquetExporter:
    """Export data to Parquet format."""
    
    def __init__(self, compression: str = "zstd"):
        self.compression = compression
    
    def export(self, df: pl.DataFrame, path: Path) -> None:
        """Write DataFrame to Parquet file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        df.write_parquet(path, compression=self.compression)


class CsvExporter:
    """Export data to CSV format."""
    
    def export(self, df: pl.DataFrame, path: Path) -> None:
        """Write DataFrame to CSV file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        df.write_csv(path)


class DataExporterFactory:
    """Factory for creating appropriate exporters based on file extension."""
    
    @staticmethod
    def create(path: Path) -> DataExporter:
        """Create an exporter based on file extension."""
        suffix = path.suffix.lower()
        
        if suffix == ".parquet":
            return ParquetExporter()
        elif suffix == ".csv":
            return CsvExporter()
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
    
    @staticmethod
    def export(df: pl.DataFrame, path: Path) -> None:
        """Convenience method to export data in one call."""
        exporter = DataExporterFactory.create(path)
        exporter.export(df, path)
