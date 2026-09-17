

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.supplier import Supplier


class SupplierRepository:
    """Repository class for Supplier model operations."""

    def __init__(self):
        """Initialize SupplierRepository."""
        self.model = Supplier

    def get(self, db: Session, supplier_id: UUID) -> Optional[Supplier]:
        """Get a supplier by UUID."""
        return db.get(Supplier, supplier_id)

    def get_by_email(self, db: Session, email: str) -> Optional[Supplier]:
        """Get a supplier by email."""
        return db.query(Supplier).filter(Supplier.email == email).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Supplier]:
        """Get all suppliers with pagination."""
        return db.query(Supplier).offset(skip).limit(limit).all()

    def create(self, db: Session, data: dict) -> Supplier:
        """Create a new supplier."""
        obj = Supplier(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: Supplier, data: dict) -> Supplier:
        """Update an existing supplier."""
        for field, value in data.items():
            if value is not None:
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Supplier) -> None:
        """Delete a supplier."""
        db.delete(db_obj)
        db.commit()


supplier_repository = SupplierRepository()

