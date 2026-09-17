from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PaymentBase(BaseModel):
    amount: Decimal
    payment_method: str
    payment_status: str
    transaction_reference: Optional[str] = None
    paid_at: datetime
    change_given: Optional[Decimal] = None
    sale_id: UUID


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    amount: Optional[Decimal] = None
    payment_method: Optional[str] = None
    payment_status: Optional[str] = None
    transaction_reference: Optional[str] = None
    paid_at: Optional[datetime] = None
    change_given: Optional[Decimal] = None
    sale_id: Optional[UUID] = None


class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
