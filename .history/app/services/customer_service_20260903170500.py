from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.customer_repository import customer_repository
from app.schemas.customer import CustomerCreate, CustomerUpdate


def get_customer(db: Session, customer_id: UUID):
    """Get a customer by ID."""
    customer = customer_repository.get(db, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer


def list_customers(db: Session):
    """List all customers."""
    return customer_repository.get_all(db)


def create_customer(db: Session, data: CustomerCreate):
    """Create a new customer."""
    return customer_repository.create(db, data.model_dump())


def update_customer(db: Session, customer_id: UUID, data: CustomerUpdate):
    """Update an existing customer."""
    customer = get_customer(db, customer_id)
    return customer_repository.update(db, customer, data.model_dump(exclude_unset=True))


def delete_customer(db: Session, customer_id: UUID):
    """Delete a customer."""
    customer = get_customer(db, customer_id)
    customer_repository.delete(db, customer)