"""Supplier schema module."""

from datetime import datetime
from uuid import UUID
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SupplierBase(BaseModel):
    """Base supplier schema."""
    company_name: str = Field(..., min_length=1, max_length=200)
    contact_name: Optional[str] = Field(None, max_length=200)
    email: Optional[str] = Field(None, max_length=150)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    tax_id: Optional[str] = Field(None, max_length=50)
    license_number: Optional[str] = Field(None, max_length=50)
    payment_terms: Optional[str] = Field(None, max_length=50)
    lead_time_days: Optional[int] = Field(None, ge=0)
    minimum_order_amount: Optional[Decimal] = Field(None, ge=0)
    is_active: bool = True


class SupplierCreate(SupplierBase):
    """Supplier creation schema."""
    pass


class SupplierUpdate(BaseModel):
    """Supplier update schema."""
    company_name: Optional[str] = Field(None, min_length=1, max_length=200)
    contact_name: Optional[str] = Field(None, max_length=200)
    email: Optional[str] = Field(None, max_length=150)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    tax_id: Optional[str] = Field(None, max_length=50)
    license_number: Optional[str] = Field(None, max_length=50)
    payment_terms: Optional[str] = Field(None, max_length=50)
    lead_time_days: Optional[int] = Field(None, ge=0)
    minimum_order_amount: Optional[Decimal] = Field(None, ge=0)
    is_active: Optional[bool] = None


class SupplierRead(SupplierBase):
    """Supplier read schema."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime