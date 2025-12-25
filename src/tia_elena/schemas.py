"""
Pydantic schemas for data validation.

These models define the expected structure of input and output data,
enabling runtime validation and clear documentation.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from dataclasses import dataclass


class RemunerationRecord(BaseModel):
    """Schema for a single remuneration input record."""
    
    employee_id: str
    local_currency: str = Field(min_length=1, max_length=10)
    remuneration_concept: str
    local_amount: float
    bonus_target_pct: float = Field(ge=0, le=1)
    subsidiary_code: str
    
    @field_validator("local_currency")
    @classmethod
    def strip_currency(cls, v: str) -> str:
        return v.strip()


class FxRate(BaseModel):
    """Schema for a currency exchange rate record."""
    
    currency: str = Field(min_length=2, max_length=5)
    fx_rate_to_eur: float = Field(gt=0)


class ConceptMapping(BaseModel):
    """Schema for concept-to-category mapping."""
    
    concept_raw: str
    category_normalized: str


class BonusPool(BaseModel):
    """Schema for subsidiary bonus pool allocation."""
    
    subsidiary_code: str
    pool_amount_eur: float = Field(ge=0)


class ProcessedRecord(BaseModel):
    """Schema for a processed output record."""
    
    employee_id: str
    subsidiary_code: str
    category_normalized: str
    theoretical_eur: float
    funding_ratio: float = Field(ge=0, le=1.01)
    final_payout_eur: float


@dataclass
class ValidationError:
    """A single validation error."""
    row: int
    column: str
    value: str
    error: str


@dataclass
class ValidationResult:
    """Result of data validation."""
    is_valid: bool
    errors: List[ValidationError]
    warnings: List[str]
    rows_checked: int
    
    @property
    def error_count(self) -> int:
        return len(self.errors)
