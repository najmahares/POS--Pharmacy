import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String, nullable=False)
    payment_status = Column(String, default="completed")
    transaction_reference = Column(String, nullable=True)
    paid_at = Column(DateTime, default=datetime.now)
    change_given = Column(Numeric(10, 2), nullable=True)
    sale_id = Column(UUID(as_uuid=True), ForeignKey("sales.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    sale = relationship("Sale", back_populates="payments")

