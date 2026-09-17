"""Sale Item schema module."""

from datetime import datetime
from uuid import UUID
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SaleItemBase(BaseModel):
    """Base sale item schema."""
    quantity: Decimal = Field(..., ge=0)
    unit_price: Decimal = Field(..., ge=0)
    discount_amount: Decimal = Field(0, ge=0)
    tax_amount: Decimal = Field(..., ge=0)
    total_price: Decimal = Field(..., ge=0)
    dispense_instructions: Optional[str] = None
    refills_authorized: Optional[int] = Field(None, ge=0)
    sale_id: UUID
    product_id: UUID


class SaleItemCreate(SaleItemBase):
    """Sale item creation schema."""
    pass


class SaleItemUpdate(BaseModel):
    """Sale item update schema."""
    quantity: Optional[Decimal] = Field(None, ge=0)
    unit_price: Optional[Decimal] = Field(None, ge=0)
    discount_amount: Optional[Decimal] = Field(None, ge=0)
    tax_amount: Optional[Decimal] = Field(None, ge=0)
    total_price: Optional[Decimal] = Field(None, ge=0)
    dispense_instructions: Optional[str] = None
    refills_authorized: Optional[int] = Field(None, ge=0)
    sale_id: Optional[UUID] = None
    product_id: Optional[UUID] = None


class SaleItemRead(SaleItemBase):
    """Sale item read schema."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime