from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SupplierBase(BaseModel):
    company_name: str
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    license_number: Optional[str] = None
    payment_terms: Optional[str] = None
    lead_time_days: Optional[int] = None
    minimum_order_amount: Optional[Decimal] = None
    is_active: bool = True


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    license_number: Optional[str] = None
    payment_terms: Optional[str] = None
    lead_time_days: Optional[int] = None
    minimum_order_amount: Optional[Decimal] = None
    is_active: Optional[bool] = None


class SupplierRead(SupplierBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
