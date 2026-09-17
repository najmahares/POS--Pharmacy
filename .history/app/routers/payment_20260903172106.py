from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models.user import User
from app.repositories.payment_repository import payment_repository
from app.schemas.payment import PaymentCreate, PaymentRead, PaymentUpdate

router = APIRouter(prefix="/payments", tags=["payments"])

@router.get("/", response_model=List[PaymentRead])
def get_payments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return payment_repository.get_all(db, skip=skip, limit=limit)

@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(
    payment_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    payment = payment_repository.get(db, payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return payment

@router.get("/sale/{sale_id}", response_model=List[PaymentRead])
def get_payments_by_sale(
    sale_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return payment_repository.get_by_sale(db, sale_id)

@router.get("/status/{status}", response_model=List[PaymentRead])
def get_payments_by_status(
    status: str,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return payment_repository.get_by_status(db, status)

@router.post("/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def create_payment(
    data: PaymentCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return payment_repository.create(db, data.model_dump())

@router.put("/{payment_id}", response_model=PaymentRead)
def update_payment(
    payment_id: UUID,
    data: PaymentUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    payment = payment_repository.get(db, payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return payment_repository.update(db, payment, data.model_dump(exclude_unset=True))

@router.patch("/{payment_id}/status", response_model=PaymentRead)
def update_payment_status(
    payment_id: UUID,
    status: str,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    payment = payment_repository.update_status(db, payment_id, status)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return payment

@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(
    payment_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    payment = payment_repository.get(db, payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    payment_repository.delete(db, payment)
    return None