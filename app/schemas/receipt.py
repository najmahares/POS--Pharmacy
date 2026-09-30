"""Receipt schema module."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ReceiptBase(BaseModel):
    """Base receipt schema."""

    receipt_number: str = Field(..., max_length=50)
    receipt_data: dict = Field(..., description="Complete receipt data in JSON format")
    receipt_type: str = Field(..., pattern=r"^(printed|digital|both)$")
    issued_at: datetime
    sent_to_email: str | None = Field(None, max_length=150)
    pharmacist_signature: str | None = Field(None, max_length=255)
    regulatory_text: str | None = None
    sale_id: UUID


class ReceiptCreate(ReceiptBase):
    """Receipt creation schema."""


class ReceiptUpdate(BaseModel):
    """Receipt update schema."""

    receipt_number: str | None = Field(None, max_length=50)
    receipt_data: dict | None = None
    receipt_type: str | None = Field(None, pattern=r"^(printed|digital|both)$")
    issued_at: datetime | None = None
    sent_to_email: str | None = Field(None, max_length=150)
    pharmacist_signature: str | None = Field(None, max_length=255)
    regulatory_text: str | None = None
    sale_id: UUID | None = None


class ReceiptRead(ReceiptBase):
    """Receipt read schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
