"""
Configuration module for the remuneration processing system.

Uses Pydantic Settings for type-safe configuration with environment variable support.
"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with sensible defaults."""
    
    model_config = SettingsConfigDict(
        env_prefix="TIAELENA_",
        env_file=".env",
        extra="ignore"
    )
    
    # Paths
    BASE_DIR: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    DATA_DIR: Path = Field(default=Path("data"))
    
    # Input files
    INPUT_REMUNERATION: str = "input/remuneration.parquet"
    DIM_FX_RATES: str = "dim/fx_rates.parquet"
    DIM_MAPPING: str = "dim/mapping.parquet"
    DIM_BONUS_POOL: str = "dim/bonus_pool.parquet"
    
    # Output files
    OUTPUT_PROCESSED: str = "output/processed_remuneration.parquet"
    OUTPUT_AUDIT: str = "output/audit_pool_adjustment.parquet"
    OUTPUT_CSV_EXPORT: str = "output/processed_remuneration.csv"
    
    # Business rules
    FUNDING_RATIO_CAP: float = 1.0
    DEFAULT_FUNDING_RATIO: float = 1.0
    UNMAPPED_CATEGORY: str = "UNMAPPED"
    
    # Performance
    CHUNK_SIZE: int = 100_000
    
    @property
    def input_path(self) -> Path:
        return self.DATA_DIR / self.INPUT_REMUNERATION
    
    @property
    def fx_rates_path(self) -> Path:
        return self.DATA_DIR / self.DIM_FX_RATES
    
    @property
    def mapping_path(self) -> Path:
        return self.DATA_DIR / self.DIM_MAPPING
    
    @property
    def bonus_pool_path(self) -> Path:
        return self.DATA_DIR / self.DIM_BONUS_POOL
    
    @property
    def output_path(self) -> Path:
        return self.DATA_DIR / self.OUTPUT_PROCESSED
    
    @property
    def audit_path(self) -> Path:
        return self.DATA_DIR / self.OUTPUT_AUDIT


# Singleton instance
settings = Settings()
