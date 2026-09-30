"""Sale schema module."""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SaleBase(BaseModel):
    """Base sale schema."""

    sale_number: str = Field(..., max_length=50)
    sale_date: datetime
    subtotal: Decimal = Field(..., ge=0)
    tax_amount: Decimal = Field(..., ge=0)
    discount_amount: Decimal = Field(0, ge=0)
    total_amount: Decimal = Field(..., ge=0)
    status: str = Field(
        ..., pattern=r"^(completed|pending|cancelled|refunded|partially-refunded)$"
    )
    prescription_number: str | None = Field(None, max_length=50)
    prescribing_doctor: str | None = Field(None, max_length=200)
    dispense_date: date | None = None
    notes: str | None = None
    customer_id: UUID | None = None
    user_id: UUID | None = None


class SaleCreate(SaleBase):
    """Sale creation schema."""


class SaleUpdate(BaseModel):
    """Sale update schema."""

    sale_number: str | None = Field(None, max_length=50)
    sale_date: datetime | None = None
    subtotal: Decimal | None = Field(None, ge=0)
    tax_amount: Decimal | None = Field(None, ge=0)
    discount_amount: Decimal | None = Field(None, ge=0)
    total_amount: Decimal | None = Field(None, ge=0)
    status: str | None = Field(
        None, pattern=r"^(completed|pending|cancelled|refunded|partially-refunded)$"
    )
    prescription_number: str | None = Field(None, max_length=50)
    prescribing_doctor: str | None = Field(None, max_length=200)
    dispense_date: date | None = None
    notes: str | None = None
    customer_id: UUID | None = None
    user_id: UUID | None = None


class SaleRead(SaleBase):
    """Sale read schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
