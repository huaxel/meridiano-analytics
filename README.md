# tia-elena 🏦

Variable Remuneration Processing System for Global Banking.

A high-performance ETL system for processing variable remuneration data with realistic banking context, including regulatory compliance (CRD IV/V), multi-currency support, and professional visualization.

## Features

- **High Performance**: Polars + Parquet = 0.13s for 320K+ rows
- **Banking Context**: MRTs, deferred compensation, clawbacks, LTIP
- **Global Support**: 20 subsidiaries, 14 currencies, garbage data simulation
- **Validation**: Pydantic schemas with input validation
- **Dashboard**: Streamlit C-Suite dashboard with regulatory KPIs

## Installation

```bash
# Clone and install
git clone <repo>
cd tia-elena
uv sync

# Or install in editable mode
uv pip install -e .
```

## Usage

### CLI Commands

```bash
# Generate synthetic data (190K employees, 320K records)
tia-elena generate

# Run ETL pipeline
tia-elena etl

# Launch dashboard
tia-elena dashboard
```

### As a Library

```python
from tia_elena import run_pipeline, settings

# Run ETL
result = run_pipeline()
print(f"Processed {result.rows_processed} rows in {result.execution_time_seconds:.2f}s")

# Custom paths
from tia_elena.pipeline import ETLPipeline
pipeline = ETLPipeline(input_path=Path("custom/input.parquet"))
result = pipeline.run()
```

## Project Structure

```
src/tia_elena/
├── config.py           # Pydantic Settings
├── schemas.py          # Validation models
├── validation.py       # Input validation
├── loaders.py          # Data loaders (Protocol pattern)
├── transformers.py     # Pure transformation functions
├── calculators.py      # Business logic
├── exporters.py        # Data exporters
├── pipeline.py         # ETL orchestrator
├── cli.py              # CLI entry points
├── generators/         # Data generation
│   ├── config.py       # Bank configuration
│   ├── employees.py    # Employee generation
│   ├── remuneration.py # Remuneration generation
│   ├── garbage.py      # Data quality issues
│   └── dimensions.py   # Dimension tables
└── dashboard/          # Streamlit app
    ├── theme.py        # Colors, CSS
    ├── charts.py       # Chart factories
    ├── data.py         # Data loading
    └── app.py          # Main dashboard
```

## Architecture

- **SOLID**: Single responsibility, Open/Closed with Protocols
- **GoF Patterns**: Strategy (loaders/exporters), Factory, Pipeline
- **GRASP**: Information Expert, Low Coupling, High Cohesion
- **DRY**: Centralized config, reusable components

## Testing

```bash
pytest tests/ -v
```

## License

MIT
