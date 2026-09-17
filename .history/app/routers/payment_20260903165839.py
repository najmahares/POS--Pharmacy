from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.repositories.payment_repository import payment_repository
from app.schemas.payment import PaymentCreate, PaymentRead, PaymentUpdate

router = APIRouter()

@router.get("/", response_model=List[PaymentRead])
def get_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return payment_repository.get_all(db, skip, limit)

@router.post("/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return payment_repository.create(db, data.model_dump())

@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    payment = payment_repository.get(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.put("/{payment_id}", response_model=PaymentRead)
def update_payment(payment_id: UUID, data: PaymentUpdate, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    payment = payment_repository.get(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment_repository.update(db, payment, data.model_dump(exclude_unset=True))

@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    payment = payment_repository.get(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment_repository.delete(db, payment)
