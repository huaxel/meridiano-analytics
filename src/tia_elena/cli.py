"""
CLI entry points for tia-elena.
"""
import sys
from pathlib import Path


def generate():
    """Generate synthetic data."""
    from tia_elena.generators import generate_employees, generate_remuneration, generate_dimension_tables
    from tia_elena.config import settings
    
    print("=" * 60)
    print("Banco Meridiano: Data Generation")
    print("=" * 60)
    
    # Ensure directories
    (settings.DATA_DIR / "input").mkdir(parents=True, exist_ok=True)
    (settings.DATA_DIR / "dim").mkdir(parents=True, exist_ok=True)
    (settings.DATA_DIR / "output").mkdir(parents=True, exist_ok=True)
    
    # Generate
    print("Generating employees...")
    employees = generate_employees()
    print(f"  ✓ {len(employees):,} employees")
    
    print("Generating remuneration records...")
    remuneration = generate_remuneration(employees)
    remuneration.write_parquet(settings.input_path)
    print(f"  ✓ {len(remuneration):,} records")
    
    print("Generating dimension tables...")
    employees.write_parquet(settings.DATA_DIR / "dim" / "employees.parquet")
    generate_dimension_tables(settings.DATA_DIR)
    print("  ✓ Done")
    
    print("=" * 60)


def etl():
    """Run ETL pipeline."""
    from tia_elena import run_pipeline
    
    print("=" * 60)
    print("tia-elena: ETL Pipeline")
    print("=" * 60)
    
    result = run_pipeline()
    
    print(f"\n✓ Rows: {result.rows_processed:,}")
    print(f"✓ Time: {result.execution_time_seconds:.2f}s")
    print(f"✓ Output: {result.output_path}")
    print("=" * 60)


def dashboard():
    """Launch Streamlit dashboard."""
    import subprocess
    app_path = Path(__file__).parent / "dashboard" / "app.py"
    subprocess.run(["streamlit", "run", str(app_path)])


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: tia-elena <command>")
        print("Commands: generate, etl, dashboard")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "generate":
        generate()
    elif command == "etl":
        etl()
    elif command == "dashboard":
        dashboard()
    else:
        print(f"Unknown command: {command}")
        print("Commands: generate, etl, dashboard")
        sys.exit(1)


if __name__ == "__main__":
    main()
