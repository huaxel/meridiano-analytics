"""
Pydantic schemas for data validation.

These models define the expected structure of input and output data,
enabling runtime validation and clear documentation.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class RemunerationRecord(BaseModel):
    """Schema for a single remuneration input record."""
    
    employee_id: str
    local_currency: str = Field(min_length=3, max_length=3)
    remuneration_concept: str
    local_amount: float = Field(gt=0)
    bonus_target_pct: float = Field(ge=0, le=1)
    subsidiary_code: int = Field(gt=0)
    
    @field_validator("local_currency")
    @classmethod
    def uppercase_currency(cls, v: str) -> str:
        return v.upper()


class FxRate(BaseModel):
    """Schema for a currency exchange rate record."""
    
    currency: str = Field(min_length=3, max_length=3)
    fx_rate_to_eur: float = Field(gt=0)


class ConceptMapping(BaseModel):
    """Schema for concept-to-category mapping."""
    
    concept_raw: str
    category_normalized: str


class BonusPool(BaseModel):
    """Schema for subsidiary bonus pool allocation."""
    
    subsidiary_code: int = Field(gt=0)
    pool_amount_eur: float = Field(ge=0)


class ProcessedRecord(BaseModel):
    """Schema for a processed output record."""
    
    employee_id: str
    subsidiary_code: int
    category_normalized: str
    theoretical_eur: float
    funding_ratio: float = Field(ge=0, le=1)
    final_payout_eur: float = Field(ge=0)


class PoolAuditRecord(BaseModel):
    """Schema for pool audit trail record."""
    
    subsidiary_code: int
    pool_amount_eur: float
    total_needed_eur: float
    funding_ratio: float
