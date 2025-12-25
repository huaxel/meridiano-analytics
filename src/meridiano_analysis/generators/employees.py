"""
Employee data generator.
"""
import polars as pl
import numpy as np
import random

from .config import SUBSIDIARIES, JOB_LEVELS


def generate_employees(seed: int = 42) -> pl.DataFrame:
    """Generate employee master data."""
    np.random.seed(seed)
    random.seed(seed)
    
    employees = []
    emp_id = 0
    
    for sub_code, sub_info in SUBSIDIARIES.items():
        for _ in range(sub_info["employees"]):
            level = np.random.choice(
                list(JOB_LEVELS.keys()),
                p=[JOB_LEVELS[l]["pct"] for l in JOB_LEVELS]
            )
            level_info = JOB_LEVELS[level]
            base = np.random.uniform(level_info["min"], level_info["max"])
            
            employees.append({
                "employee_id": f"EMP{emp_id:08d}",
                "subsidiary_code": sub_code,
                "job_level": level,
                "is_mrt": level_info["mrt_eligible"] and random.random() < 0.3,
                "base_salary_eur": round(base, 2),
                "local_currency": sub_info["currency"],
            })
            emp_id += 1
    
    return pl.DataFrame(employees)
