from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SaleItemBase(BaseModel):
    quantity: Decimal
    unit_price: Decimal
    discount_amount: Decimal = 0
    tax_amount: Decimal
    total_price: Decimal
    dispense_instructions: Optional[str] = None
    refills_authorized: Optional[int] = None
    sale_id: UUID
    product_id: UUID


class SaleItemCreate(SaleItemBase):
    pass


class SaleItemUpdate(BaseModel):
    quantity: Optional[Decimal] = None
    unit_price: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    total_price: Optional[Decimal] = None
    dispense_instructions: Optional[str] = None
    refills_authorized: Optional[int] = None
    sale_id: Optional[UUID] = None
    product_id: Optional[UUID] = None


class SaleItemRead(SaleItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
