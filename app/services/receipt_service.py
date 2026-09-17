"""Receipt service module."""

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.receipt_repository import receipt_repository
from app.schemas.receipt import ReceiptCreate, ReceiptUpdate


def get_receipt(db: Session, receipt_id: UUID):
    """Get a receipt by ID."""
    receipt = receipt_repository.get(db, receipt_id)
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found"
        )
    return receipt


def list_receipts(db: Session):
    """List all receipts."""
    return receipt_repository.get_all(db)


def create_receipt(db: Session, data: ReceiptCreate):
    """Create a new receipt."""
    return receipt_repository.create(db, data.model_dump())


def update_receipt(db: Session, receipt_id: UUID, data: ReceiptUpdate):
    """Update an existing receipt."""
    receipt = get_receipt(db, receipt_id)
    return receipt_repository.update(db, receipt, data.model_dump(exclude_unset=True))


def delete_receipt(db: Session, receipt_id: UUID):
    """Delete a receipt."""
    receipt = get_receipt(db, receipt_id)
    receipt_repository.delete(db, receipt)
