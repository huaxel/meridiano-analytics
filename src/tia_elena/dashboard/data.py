"""
Data loading for dashboard.
"""
import streamlit as st
import polars as pl

from tia_elena.config import settings


@st.cache_data
def load_processed_data() -> pl.DataFrame:
    """Load processed remuneration data."""
    if not settings.output_path.exists():
        raise FileNotFoundError(
            f"Data not found: {settings.output_path}\n"
            "Run: tia-elena generate && tia-elena etl"
        )
    return pl.read_parquet(settings.output_path)


@st.cache_data
def load_audit_data() -> pl.DataFrame | None:
    """Load audit data if available."""
    if settings.audit_path.exists():
        return pl.read_parquet(settings.audit_path)
    return None
