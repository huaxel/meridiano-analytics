"""
Data generators package.

Generates realistic synthetic data for a global Spanish bank.
"""
from .config import SUBSIDIARIES, REMUNERATION_CONCEPTS, JOB_LEVELS, FX_RATES
from .employees import generate_employees
from .remuneration import generate_remuneration
from .dimensions import generate_dimension_tables

__all__ = [
    "SUBSIDIARIES",
    "REMUNERATION_CONCEPTS",
    "JOB_LEVELS",
    "FX_RATES",
    "generate_employees",
    "generate_remuneration",
    "generate_dimension_tables",
]
