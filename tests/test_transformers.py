"""
Tests for transformer functions.
"""
import polars as pl
from tia_elena.transformers import explode_concepts, enrich_with_fx, enrich_with_mapping


def test_explode_concepts_single(sample_remuneration_df):
    """Single concept should remain unchanged."""
    df = sample_remuneration_df.filter(pl.col("employee_id") == "emp1").lazy()
    result = explode_concepts(df).collect()
    
    assert len(result) == 1
    assert result["local_amount"][0] == 10000.0
    assert result["remuneration_concept"][0] == "BONUS_ANUAL_CASH"


def test_explode_concepts_combined(sample_remuneration_df):
    """Combined concepts should be split with proportional amounts."""
    df = sample_remuneration_df.filter(pl.col("employee_id") == "emp2").lazy()
    result = explode_concepts(df).collect()
    
    assert len(result) == 2
    assert result["local_amount"].sum() == 20000.0
    assert set(result["remuneration_concept"].to_list()) == {"BONUS_ANUAL_CASH", "LTIP_PERFORMANCE"}


def test_enrich_with_fx(sample_remuneration_df, sample_fx_rates_df):
    """FX enrichment should calculate EUR amounts correctly."""
    df = sample_remuneration_df.filter(pl.col("employee_id") == "emp1").lazy()
    fx = sample_fx_rates_df.lazy()
    
    result = enrich_with_fx(df, fx).collect()
    
    # 10000 USD * 0.92 = 9200 EUR
    assert abs(result["theoretical_eur"][0] - 9200.0) < 0.01


def test_enrich_with_mapping(sample_remuneration_df, sample_mapping_df):
    """Mapping enrichment should normalize categories."""
    df = sample_remuneration_df.filter(pl.col("employee_id") == "emp1").lazy()
    mapping = sample_mapping_df.lazy()
    
    result = enrich_with_mapping(df, mapping).collect()
    
    assert result["category_normalized"][0] == "Bonus Anual"


def test_enrich_with_mapping_unmapped(sample_remuneration_df, sample_mapping_df):
    """Unmapped concepts should get default value."""
    df = pl.DataFrame({
        "employee_id": ["x"],
        "remuneration_concept": ["UNKNOWN_CONCEPT"],
    }).lazy()
    mapping = sample_mapping_df.lazy()
    
    result = enrich_with_mapping(df, mapping, unmapped_value="NO_MATCH").collect()
    
    assert result["category_normalized"][0] == "NO_MATCH"
