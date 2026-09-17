"""Customer repository module for database operations."""

from uuid import UUID
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerRepository:
    """Repository class for Customer model operations."""

    def __init__(self):
        """Initialize CustomerRepository."""
        self.model = Customer

    def get(self, db: Session, customer_id: UUID) -> Optional[Customer]:
        """Get a customer by UUID."""
        return db.get(Customer, customer_id)

    def get_by_email(self, db: Session, email: str) -> Optional[Customer]:
        """Get a customer by email."""
        return db.query(Customer).filter(Customer.email == email).first()

    def get_by_medical_record(self, db: Session, medical_record_number: str) -> Optional[Customer]:
        """Get a customer by medical record number."""
        return db.query(Customer).filter(
            Customer.medical_record_number == medical_record_number
        ).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Customer]:
        """Get all customers with pagination."""
        return db.query(Customer).offset(skip).limit(limit).all()

    def create(self, db: Session, data: dict) -> Customer:
        """Create a new customer."""
        obj = Customer(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: Customer, data: dict) -> Customer:
        """Update an existing customer."""
        for field, value in data.items():
            if value is not None:
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Customer) -> None:
        """Delete a customer."""
        db.delete(db_obj)
        db.commit()


customer_repository = CustomerRepository()