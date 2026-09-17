import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    receipt_number = Column(String, unique=True, index=True, nullable=False)
    receipt_type = Column(String, default="standard")
    issued_at = Column(DateTime, default=datetime.now)
    pharmacist_signature = Column(String, nullable=True)
    regulatory_text = Column(String, nullable=True)

    sale_id = Column(UUID(as_uuid=True), ForeignKey("sales.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    sale = relationship("Sale", back_populates="receipts")

