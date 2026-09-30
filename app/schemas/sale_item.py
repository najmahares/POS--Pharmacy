"""Sale Item schema module."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SaleItemBase(BaseModel):
    """Base sale item schema."""

    quantity: Decimal = Field(..., ge=0)
    unit_price: Decimal = Field(..., ge=0)
    discount_amount: Decimal = Field(0, ge=0)
    tax_amount: Decimal = Field(..., ge=0)
    total_price: Decimal = Field(..., ge=0)
    dispense_instructions: str | None = None
    refills_authorized: int | None = Field(None, ge=0)
    sale_id: UUID
    product_id: UUID


class SaleItemCreate(SaleItemBase):
    """Sale item creation schema."""


class SaleItemUpdate(BaseModel):
    """Sale item update schema."""

    quantity: Decimal | None = Field(None, ge=0)
    unit_price: Decimal | None = Field(None, ge=0)
    discount_amount: Decimal | None = Field(None, ge=0)
    tax_amount: Decimal | None = Field(None, ge=0)
    total_price: Decimal | None = Field(None, ge=0)
    dispense_instructions: str | None = None
    refills_authorized: int | None = Field(None, ge=0)
    sale_id: UUID | None = None
    product_id: UUID | None = None


class SaleItemRead(SaleItemBase):
    """Sale item read schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
