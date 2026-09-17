"""Customer router module."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models.user import User
from app.repositories.customer_repository import customer_repository
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/", response_model=List[CustomerRead])
def get_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Get all customers with pagination."""
    return customer_repository.get_all(db, skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Get a specific customer by ID."""
    customer = customer_repository.get(db, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer


@router.get("/email/{email}", response_model=CustomerRead)
def get_customer_by_email(
    email: str,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Get a customer by email."""
    customer = customer_repository.get_by_email(db, email)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer


@router.get("/medical-record/{medical_record_number}", response_model=CustomerRead)
def get_customer_by_medical_record(
    medical_record_number: str,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Get a customer by medical record number."""
    customer = customer_repository.get_by_medical_record(db, medical_record_number)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer


@router.post("/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(
    data: CustomerCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Create a new customer."""
    # Check if email already exists
    if data.email:
        existing = customer_repository.get_by_email(db, data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    # Check if medical record number already exists
    if data.medical_record_number:
        existing = customer_repository.get_by_medical_record(db, data.medical_record_number)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Medical record number already exists"
            )

    return customer_repository.create(db, data.model_dump())


@router.put("/{customer_id}", response_model=CustomerRead)
def update_customer(
    customer_id: UUID,
    data: CustomerUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Update an existing customer."""
    customer = customer_repository.get(db, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer_repository.update(db, customer, data.model_dump(exclude_unset=True))


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    """Delete a customer. Requires admin role."""
    customer = customer_repository.get(db, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    customer_repository.delete(db, customer)
    return None