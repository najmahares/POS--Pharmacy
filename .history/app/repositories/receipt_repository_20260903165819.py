
from uuid import UUID
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.receipt import Receipt


class ReceiptRepository:
    """Repository class for Receipt model operations."""

    def __init__(self):
        """Initialize ReceiptRepository."""
        self.model = Receipt

    def get(self, db: Session, receipt_id: UUID) -> Optional[Receipt]:
        """Get a receipt by UUID."""
        return db.get(Receipt, receipt_id)

    def get_by_receipt_number(self, db: Session, receipt_number: str) -> Optional[Receipt]:
        """Get a receipt by receipt number."""
        return db.query(Receipt).filter(Receipt.receipt_number == receipt_number).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Receipt]:
        """Get all receipts with pagination."""
        return db.query(Receipt).offset(skip).limit(limit).all()

    def get_by_sale(self, db: Session, sale_id: UUID) -> Optional[Receipt]:
        """Get a receipt by sale ID."""
        return db.query(Receipt).filter(Receipt.sale_id == sale_id).first()

    def create(self, db: Session, data: dict) -> Receipt:
        """Create a new receipt."""
        obj = Receipt(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: Receipt, data: dict) -> Receipt:
        """Update an existing receipt."""
        for field, value in data.items():
            if value is not None:
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Receipt) -> None:
        """Delete a receipt."""
        db.delete(db_obj)
        db.commit()


receipt_repository = ReceiptRepository()