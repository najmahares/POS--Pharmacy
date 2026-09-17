"""Supplier service module."""

from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.supplier_repository import supplier_repository
from app.schemas.supplier import SupplierCreate, SupplierUpdate


def get_supplier(db: Session, supplier_id: UUID):
    """Get a supplier by ID."""
    supplier = supplier_repository.get(db, supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    return supplier


def list_suppliers(db: Session):
    """List all suppliers."""
    return supplier_repository.get_all(db)


def create_supplier(db: Session, data: SupplierCreate):
    """Create a new supplier."""
    return supplier_repository.create(db, data.model_dump())


def update_supplier(db: Session, supplier_id: UUID, data: SupplierUpdate):
    """Update an existing supplier."""
    supplier = get_supplier(db, supplier_id)
    return supplier_repository.update(db, supplier, data.model_dump(exclude_unset=True))


def delete_supplier(db: Session, supplier_id: UUID):
    """Delete a supplier."""
    supplier = get_supplier(db, supplier_id)
    supplier_repository.delete(db, supplier)