"""Sale schema module."""

from datetime import datetime, date
from uuid import UUID
from typing import Optional, List
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SaleBase(BaseModel):
    """Base sale schema."""
    sale_number: str = Field(..., max_length=50)
    sale_date: datetime
    subtotal: Decimal = Field(..., ge=0)
    tax_amount: Decimal = Field(..., ge=0)
    discount_amount: Decimal = Field(0, ge=0)
    total_amount: Decimal = Field(..., ge=0)
    status: str = Field(..., pattern=r"^(completed|pending|cancelled|refunded|partially-refunded)$")
    prescription_number: Optional[str] = Field(None, max_length=50)
    prescribing_doctor: Optional[str] = Field(None, max_length=200)
    dispense_date: Optional[date] = None
    notes: Optional[str] = None
    customer_id: Optional[UUID] = None
    user_id: UUID


class SaleCreate(SaleBase):
    """Sale creation schema."""
    pass


class SaleUpdate(BaseModel):
    """Sale update schema."""
    sale_number: Optional[str] = Field(None, max_length=50)
    sale_date: Optional[datetime] = None
    subtotal: Optional[Decimal] = Field(None, ge=0)
    tax_amount: Optional[Decimal] = Field(None, ge=0)
    discount_amount: Optional[Decimal] = Field(None, ge=0)
    total_amount: Optional[Decimal] = Field(None, ge=0)
    status: Optional[str] = Field(None, pattern=r"^(completed|pending|cancelled|refunded|partially-refunded)$")
    prescription_number: Optional[str] = Field(None, max_length=50)
    prescribing_doctor: Optional[str] = Field(None, max_length=200)
    dispense_date: Optional[date] = None
    notes: Optional[str] = None
    customer_id: Optional[UUID] = None
    user_id: Optional[UUID] = None


class SaleRead(SaleBase):
    """Sale read schema."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    receipt_id: UUID
    created_at: datetime
    updated_at: datetime
    items: Optional[List['SaleItemRead']] = None
    payments: Optional[List['PaymentRead']] = None


from app.schemas.sale_item import SaleItemRead
from app.schemas.payment import PaymentRead
SaleRead.model_rebuild()