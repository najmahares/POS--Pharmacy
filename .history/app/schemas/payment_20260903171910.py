"""Payment schema module."""

from datetime import datetime
from uuid import UUID
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PaymentBase(BaseModel):
    """Base payment schema."""
    amount: Decimal = Field(..., ge=0)
    payment_method: str = Field(..., pattern=r"^(cash|credit-card|debit-card|mobile-wallet|insurance-claim|gift-card|bank-transfer)$")
    payment_status: str = Field(..., pattern=r"^(pending|completed|failed|refunded|partially-refunded)$")
    transaction_reference: Optional[str] = Field(None, max_length=100)
    paid_at: datetime
    change_given: Optional[Decimal] = Field(None, ge=0)
    sale_id: UUID


class PaymentCreate(PaymentBase):
    """Payment creation schema."""
    pass


class PaymentUpdate(BaseModel):
    """Payment update schema."""
    amount: Optional[Decimal] = Field(None, ge=0)
    payment_method: Optional[str] = Field(None, pattern=r"^(cash|credit-card|debit-card|mobile-wallet|insurance-claim|gift-card|bank-transfer)$")
    payment_status: Optional[str] = Field(None, pattern=r"^(pending|completed|failed|refunded|partially-refunded)$")
    transaction_reference: Optional[str] = Field(None, max_length=100)
    paid_at: Optional[datetime] = None
    change_given: Optional[Decimal] = Field(None, ge=0)
    sale_id: Optional[UUID] = None


class PaymentRead(PaymentBase):
    """Payment read schema."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime