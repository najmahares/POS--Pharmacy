"""Receipt schema module."""

from datetime import datetime
from uuid import UUID
from typing import Optional, Any

from pydantic import BaseModel, ConfigDict, Field


class ReceiptBase(BaseModel):
    """Base receipt schema."""
    receipt_number: str = Field(..., max_length=50)
    receipt_data: dict = Field(..., description="Complete receipt data in JSON format")
    receipt_type: str = Field(..., pattern=r"^(printed|digital|both)$")
    issued_at: datetime
    sent_to_email: Optional[str] = Field(None, max_length=150)
    pharmacist_signature: Optional[str] = Field(None, max_length=255)
    regulatory_text: Optional[str] = None
    sale_id: UUID


class ReceiptCreate(ReceiptBase):
    """Receipt creation schema."""
    pass


class ReceiptUpdate(BaseModel):
    """Receipt update schema."""
    receipt_number: Optional[str] = Field(None, max_length=50)
    receipt_data: Optional[dict] = None
    receipt_type: Optional[str] = Field(None, pattern=r"^(printed|digital|both)$")
    issued_at: Optional[datetime] = None
    sent_to_email: Optional[str] = Field(None, max_length=150)
    pharmacist_signature: Optional[str] = Field(None, max_length=255)
    regulatory_text: Optional[str] = None
    sale_id: Optional[UUID] = None


class ReceiptRead(ReceiptBase):
    """Receipt read schema."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime