
from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.sale import Sale


class SaleRepository:
    """Repository class for Sale model operations."""

    def __init__(self):
        """Initialize SaleRepository."""
        self.model = Sale

    def get(self, db: Session, sale_id: UUID) -> Optional[Sale]:
        """Get a sale by UUID."""
        return db.get(Sale, sale_id)

    def get_by_sale_number(self, db: Session, sale_number: str) -> Optional[Sale]:
        """Get a sale by sale number."""
        return db.query(Sale).filter(Sale.sale_number == sale_number).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Sale]:
        """Get all sales with pagination."""
        return db.query(Sale).offset(skip).limit(limit).all()

    def get_by_customer(self, db: Session, customer_id: UUID) -> List[Sale]:
        """Get all sales by customer."""
        return db.query(Sale).filter(Sale.customer_id == customer_id).all()

    def get_by_user(self, db: Session, user_id: UUID) -> List[Sale]:
        """Get all sales by user."""
        return db.query(Sale).filter(Sale.user_id == user_id).all()

    def get_by_date_range(self, db: Session, start_date: date, end_date: date) -> List[Sale]:
        """Get sales within a date range."""
        return db.query(Sale).filter(
            Sale.sale_date >= start_date,
            Sale.sale_date <= end_date
        ).all()

    def get_by_status(self, db: Session, status: str) -> List[Sale]:
        """Get sales by status."""
        return db.query(Sale).filter(Sale.status == status).all()

    def create(self, db: Session, data: dict) -> Sale:
        """Create a new sale."""
        obj = Sale(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: Sale, data: dict) -> Sale:
        """Update an existing sale."""
        for field, value in data.items():
            if value is not None:
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Sale) -> None:
        """Delete a sale."""
        db.delete(db_obj)
        db.commit()

    def update_status(self, db: Session, sale_id: UUID, status: str) -> Sale:
        """Update sale status."""
        sale = self.get(db, sale_id)
        if sale:
            sale.status = status
            db.commit()
            db.refresh(sale)
        return sale


sale_repository = SaleRepository()

