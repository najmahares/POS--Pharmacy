"""Receipt router module."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models.user import User
from app.repositories.receipt_repository import receipt_repository
from app.schemas.receipt import ReceiptCreate, ReceiptRead, ReceiptUpdate

router = APIRouter(prefix="/receipts", tags=["receipts"])


@router.get("/", response_model=List[ReceiptRead])
def get_receipts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Get all receipts with pagination."""
    return receipt_repository.get_all(db, skip=skip, limit=limit)


@router.get("/{receipt_id}", response_model=ReceiptRead)
def get_receipt(
    receipt_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Get a specific receipt by ID."""
    receipt = receipt_repository.get(db, receipt_id)
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found"
        )
    return receipt


@router.get("/receipt-number/{receipt_number}", response_model=ReceiptRead)
def get_receipt_by_receipt_number(
    receipt_number: str,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Get a receipt by receipt number."""
    receipt = receipt_repository.get_by_receipt_number(db, receipt_number)
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found"
        )
    return receipt


@router.get("/sale/{sale_id}", response_model=ReceiptRead)
def get_receipt_by_sale(
    sale_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Get a receipt by sale ID."""
    receipt = receipt_repository.get_by_sale(db, sale_id)
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found"
        )
    return receipt


@router.post("/", response_model=ReceiptRead, status_code=status.HTTP_201_CREATED)
def create_receipt(
    data: ReceiptCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Create a new receipt."""
    return receipt_repository.create(db, data.model_dump())


@router.put("/{receipt_id}", response_model=ReceiptRead)
def update_receipt(
    receipt_id: UUID,
    data: ReceiptUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    """Update an existing receipt. Requires admin role."""
    receipt = receipt_repository.get(db, receipt_id)
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found"
        )
    return receipt_repository.update(db, receipt, data.model_dump(exclude_unset=True))


@router.delete("/{receipt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_receipt(
    receipt_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    """Delete a receipt. Requires admin role."""
    receipt = receipt_repository.get(db, receipt_id)
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found"
        )
    receipt_repository.delete(db, receipt)
    return None