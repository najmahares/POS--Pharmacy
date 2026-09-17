from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.repositories.customer_repository import customer_repository
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate

router = APIRouter()

@router.get("/", response_model=List[CustomerRead])
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return customer_repository.get_all(db, skip, limit)

@router.post("/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return customer_repository.create(db, data.model_dump())

@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    customer = customer_repository.get(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=CustomerRead)
def update_customer(customer_id: UUID, data: CustomerUpdate, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    customer = customer_repository.get(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer_repository.update(db, customer, data.model_dump(exclude_unset=True))

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    customer = customer_repository.get(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer_repository.delete(db, customer)
