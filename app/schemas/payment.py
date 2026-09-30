"""Payment schema module."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PaymentBase(BaseModel):
    """Base payment schema."""

    amount: Decimal = Field(..., ge=0)
    payment_method: str = Field(
        ...,
        pattern=r"^(cash|credit-card|debit-card|mobile-wallet|insurance-claim|gift-card|bank-transfer)$",
    )
    payment_status: str = Field(
        ..., pattern=r"^(pending|completed|failed|refunded|partially-refunded)$"
    )
    transaction_reference: str | None = Field(None, max_length=100)
    paid_at: datetime
    change_given: Decimal | None = Field(None, ge=0)
    sale_id: UUID


class PaymentCreate(PaymentBase):
    """Payment creation schema."""


class PaymentUpdate(BaseModel):
    """Payment update schema."""

    amount: Decimal | None = Field(None, ge=0)
    payment_method: str | None = Field(
        None,
        pattern=r"^(cash|credit-card|debit-card|mobile-wallet|insurance-claim|gift-card|bank-transfer)$",
    )
    payment_status: str | None = Field(
        None, pattern=r"^(pending|completed|failed|refunded|partially-refunded)$"
    )
    transaction_reference: str | None = Field(None, max_length=100)
    paid_at: datetime | None = None
    change_given: Decimal | None = Field(None, ge=0)
    sale_id: UUID | None = None


class PaymentRead(PaymentBase):
    """Payment read schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
