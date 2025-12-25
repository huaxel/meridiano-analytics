import pytest
import polars as pl
from pathlib import Path
from unittest.mock import patch

from tia_elena.generators.remuneration import generate_remuneration
from tia_elena.generators.employees import generate_employees
from tia_elena.generators.dimensions import generate_fx_rates, generate_mapping, generate_bonus_pool
from tia_elena.pipeline import ETLPipeline
from tia_elena.exporters import DataExporterFactory

@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary data directory structure."""
    input_dir = tmp_path / "input"
    dim_dir = tmp_path / "dim"
    output_dir = tmp_path / "output"
    audit_dir = tmp_path / "audit"
    
    for d in [input_dir, dim_dir, output_dir, audit_dir]:
        d.mkdir(parents=True)
        
    return tmp_path

def test_pipeline_end_to_end(temp_data_dir):
    """
    Test the full pipeline verifying:
    1. Data generation works.
    2. ETL pipeline runs.
    3. Output parquet contains expected columns (job_level, remuneration_concept).
    """
    
    # Mock config to generate small dataset
    TEST_SUBSIDIARIES = {
        "TEST-HQ": {"name": "Test HQ", "employees": 50, "currency": "EUR", "garbage_rate": 0.0},
    }
    
    # Patch SUBSIDIARIES in both modules where it is imported
    with patch("tia_elena.generators.employees.SUBSIDIARIES", TEST_SUBSIDIARIES), \
         patch("tia_elena.generators.remuneration.SUBSIDIARIES", TEST_SUBSIDIARIES):
        
        # 1. Generate minimal data
        employees_df = generate_employees() # No count arg
        # Save employees to dim
        employees_df.write_parquet(temp_data_dir / "dim" / "employees.parquet")
        
        remuneration_df = generate_remuneration(employees_df)
        # Save remuneration to input
        remuneration_df.write_parquet(temp_data_dir / "input" / "remuneration.parquet")
        
        fx_rates = generate_fx_rates()
        pl.DataFrame(fx_rates).write_parquet(temp_data_dir / "dim" / "fx_rates.parquet")
        
        mapping = generate_mapping()
        # Ensure our generated concepts are mapped or unmapped gracefully
        pl.DataFrame(mapping).write_parquet(temp_data_dir / "dim" / "mapping.parquet")
        
        pool = generate_bonus_pool()
        pl.DataFrame(pool).write_parquet(temp_data_dir / "dim" / "bonus_pool.parquet")
        
        # 2. Run Pipeline
        pipeline = ETLPipeline(
            input_path=temp_data_dir / "input" / "remuneration.parquet",
            fx_path=temp_data_dir / "dim" / "fx_rates.parquet",
            mapping_path=temp_data_dir / "dim" / "mapping.parquet",
            pool_path=temp_data_dir / "dim" / "bonus_pool.parquet",
            output_path=temp_data_dir / "output" / "processed.parquet",
            audit_path=temp_data_dir / "audit" / "audit.parquet",
            validate=False 
        )
        
        # Manually override employees_path to point to our temp file
        pipeline.employees_path = temp_data_dir / "dim" / "employees.parquet"
        
        result = pipeline.run()
        
        # 3. Assertions
        assert result.rows_processed > 0
        assert result.output_path.exists()
        
        df_output = pl.read_parquet(result.output_path)
        columns = df_output.columns
        
        # CRITICAL CHECKS asked by user
        assert "job_level" in columns, "job_level column missing from output!"
        assert "remuneration_concept" in columns, "remuneration_concept column missing from output!"
        assert "category_normalized" in columns
        assert "final_payout_eur" in columns
        
        # Verify job_level is populated (not null)
        assert df_output.filter(pl.col("job_level").is_null()).height == 0
