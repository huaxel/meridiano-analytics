"""
tia-elena: Variable Remuneration Processing System

A high-performance ETL system for processing variable remuneration data
in a global banking context.
"""

__version__ = "0.2.0"
__author__ = "tia-elena"

from .config import settings
from .pipeline import ETLPipeline, run_pipeline, PipelineResult

__all__ = [
    "settings",
    "ETLPipeline",
    "run_pipeline",
    "PipelineResult",
]
