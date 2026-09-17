from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ReceiptBase(BaseModel):
    receipt_number: str
    receipt_data: Dict[str, Any]
    receipt_type: str
    issued_at: datetime
    pharmacist_signature: Optional[str] = None
    regulatory_text: Optional[str] = None
    sale_id: UUID


class ReceiptCreate(ReceiptBase):
    pass


class ReceiptUpdate(BaseModel):
    receipt_number: Optional[str] = None
    receipt_data: Optional[Dict[str, Any]] = None
    receipt_type: Optional[str] = None
    issued_at: Optional[datetime] = None
    pharmacist_signature: Optional[str] = None
    regulatory_text: Optional[str] = None
    sale_id: Optional[UUID] = None


class ReceiptRead(ReceiptBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
