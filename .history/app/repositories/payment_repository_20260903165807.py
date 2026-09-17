from uuid import UUID
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.payment import Payment


class PaymentRepository:
    """Repository class for Payment model operations."""

    def __init__(self):
        """Initialize PaymentRepository."""
        self.model = Payment

    def get(self, db: Session, payment_id: UUID) -> Optional[Payment]:
        """Get a payment by UUID."""
        return db.get(Payment, payment_id)

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Payment]:
        """Get all payments with pagination."""
        return db.query(Payment).offset(skip).limit(limit).all()

    def get_by_sale(self, db: Session, sale_id: UUID) -> List[Payment]:
        """Get all payments for a sale."""
        return db.query(Payment).filter(Payment.sale_id == sale_id).all()

    def get_by_status(self, db: Session, status: str) -> List[Payment]:
        """Get payments by status."""
        return db.query(Payment).filter(Payment.payment_status == status).all()

    def create(self, db: Session, data: dict) -> Payment:
        """Create a new payment."""
        obj = Payment(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: Payment, data: dict) -> Payment:
        """Update an existing payment."""
        for field, value in data.items():
            if value is not None:
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Payment) -> None:
        """Delete a payment."""
        db.delete(db_obj)
        db.commit()

    def update_status(self, db: Session, payment_id: UUID, status: str) -> Payment:
        """Update payment status."""
        payment = self.get(db, payment_id)
        if payment:
            payment.payment_status = status
            db.commit()
            db.refresh(payment)
        return payment


payment_repository = PaymentRepository()