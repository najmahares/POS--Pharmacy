"""Receipt model."""

import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    receipt_number = Column(String(50), unique=True, nullable=False)
    receipt_data = Column(JSON, nullable=True)
    receipt_type = Column(String(20), nullable=False, default="digital")
    issued_at = Column(DateTime, default=datetime.now)
    sent_to_email = Column(String(150), nullable=True)
    pharmacist_signature = Column(String(255), nullable=True)
    regulatory_text = Column(Text, nullable=True)
    sale_id = Column(UUID(as_uuid=True), ForeignKey("sales.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    sale = relationship("Sale", back_populates="receipt")
