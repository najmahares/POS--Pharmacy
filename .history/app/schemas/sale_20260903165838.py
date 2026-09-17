from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.sale_item import SaleItemRead


class SaleBase(BaseModel):
    sale_number: str
    sale_date: datetime
    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Decimal = 0
    total_amount: Decimal
    status: str
    prescription_number: Optional[str] = None
    prescribing_doctor: Optional[str] = None
    dispense_date: Optional[date] = None
    notes: Optional[str] = None
    customer_id: Optional[UUID] = None
    user_id: UUID


class SaleCreate(SaleBase):
    pass


class SaleUpdate(BaseModel):
    sale_number: Optional[str] = None
    sale_date: Optional[datetime] = None
    subtotal: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    status: Optional[str] = None
    prescription_number: Optional[str] = None
    prescribing_doctor: Optional[str] = None
    dispense_date: Optional[date] = None
    notes: Optional[str] = None
    customer_id: Optional[UUID] = None
    user_id: Optional[UUID] = None


class SaleRead(SaleBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    sale_items: List[SaleItemRead] = []
