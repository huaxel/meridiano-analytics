"""
Remuneration data generator.
"""
import polars as pl
import numpy as np
import random

from .config import SUBSIDIARIES, REMUNERATION_CONCEPTS, FX_RATES
from .garbage import (
    add_garbage_currency,
    add_garbage_concept,
    add_garbage_amount,
    add_garbage_employee_id,
)


def generate_remuneration(employees_df: pl.DataFrame, seed: int = 123) -> pl.DataFrame:
    """Generate remuneration with realistic distribution and garbage data."""
    np.random.seed(seed)
    random.seed(seed)
    
    records = []
    employees = employees_df.to_dicts()
    
    var_concepts = {k: v for k, v in REMUNERATION_CONCEPTS.items() if v.get("is_variable", False)}
    concept_list = list(var_concepts.keys())
    concept_weights = [var_concepts[c]["weight"] for c in concept_list]
    total = sum(concept_weights)
    concept_weights = [w / total for w in concept_weights]
    
    for emp in employees:
        sub_info = SUBSIDIARIES[emp["subsidiary_code"]]
        garbage_rate = sub_info["garbage_rate"]
        is_mrt = emp["is_mrt"]
        
        num_concepts = np.random.choice(
            [1, 2, 3, 4] if is_mrt else [1, 2, 3],
            p=[0.3, 0.4, 0.2, 0.1] if is_mrt else [0.5, 0.35, 0.15]
        )
        
        for _ in range(num_concepts):
            concept = np.random.choice(concept_list, p=concept_weights)
            concept_info = var_concepts[concept]
            
            pct = concept_info["avg_pct"]
            variation = np.random.uniform(0.6, 1.4)
            amount_eur = emp["base_salary_eur"] * abs(pct) * variation
            
            if pct < 0:
                amount_eur = -amount_eur
            
            fx = FX_RATES[emp["local_currency"]]
            local_amount = amount_eur / fx if fx > 0 else amount_eur
            
            is_garbage = random.random() < garbage_rate
            
            record = {
                "employee_id": add_garbage_employee_id(emp["employee_id"], emp["subsidiary_code"]) if is_garbage else emp["employee_id"],
                "subsidiary_code": emp["subsidiary_code"],
                "local_currency": add_garbage_currency(emp["local_currency"]) if is_garbage else emp["local_currency"],
                "remuneration_concept": add_garbage_concept(concept) if is_garbage else concept,
                "local_amount": round(add_garbage_amount(local_amount) if is_garbage else local_amount, 2),
                "bonus_target_pct": round(abs(pct), 2),
                "is_mrt": emp["is_mrt"],
                "is_deferred": concept_info.get("is_deferred", False),
                "is_equity": concept_info.get("is_equity", False),
            }
            records.append(record)
    
    return pl.DataFrame(records)
