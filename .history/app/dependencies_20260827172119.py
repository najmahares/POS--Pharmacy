from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.database import get_db
from app.dependencies import get_current_user, require_admin, require_pharmacist
from app.repositories.receipt_repository import receipt_repository
from app.schemas.receipt import ReceiptCreate, ReceiptUpdate, ReceiptRead

router = APIRouter()

@router.get("/", response_model=List[ReceiptRead])
def get_receipts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return receipt_repository.get_all(db, skip, limit)

@router.post("/", response_model=ReceiptRead, status_code=status.HTTP_201_CREATED)
def create_receipt(data: ReceiptCreate, db: Session = Depends(get_db), current_user: dict = Depends(require_pharmacist)):
    return receipt_repository.create(db, data.model_dump())

@router.get("/{receipt_id}", response_model=ReceiptRead)
def get_receipt(receipt_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    receipt = receipt_repository.get(db, receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt

@router.put("/{receipt_id}", response_model=ReceiptRead)
def update_receipt(receipt_id: UUID, data: ReceiptUpdate, db: Session = Depends(get_db), current_user: dict = Depends(require_pharmacist)):
    receipt = receipt_repository.get(db, receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt_repository.update(db, receipt, data.model_dump(exclude_unset=True))

@router.delete("/{receipt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_receipt(receipt_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    receipt = receipt_repository.get(db, receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    receipt_repository.delete(db, receipt)

def require_pharmacist(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in ["admin", "pharmacist"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Pharmacist privileges required"
        )
    return current_user