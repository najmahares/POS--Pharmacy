"""Sale router module."""

from typing import List
from uuid import UUID
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin, require_pharmacist
from app.models.user import User
from app.repositories.sale_repository import sale_repository
from app.schemas.sale import SaleCreate, SaleRead, SaleUpdate

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("/", response_model=List[SaleRead])
def get_sales(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Get all sales with pagination."""
    return sale_repository.get_all(db, skip=skip, limit=limit)


@router.get("/{sale_id}", response_model=SaleRead)
def get_sale(
    sale_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Get a specific sale by ID."""
    sale = sale_repository.get(db, sale_id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    return sale


@router.get("/sale-number/{sale_number}", response_model=SaleRead)
def get_sale_by_sale_number(
    sale_number: str,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Get a sale by sale number."""
    sale = sale_repository.get_by_sale_number(db, sale_number)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    return sale


@router.get("/customer/{customer_id}", response_model=List[SaleRead])
def get_sales_by_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Get all sales for a customer."""
    return sale_repository.get_by_customer(db, customer_id)


@router.get("/user/{user_id}", response_model=List[SaleRead])
def get_sales_by_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    """Get all sales by a user. Requires admin role."""
    return sale_repository.get_by_user(db, user_id)


@router.get("/date-range/", response_model=List[SaleRead])
def get_sales_by_date_range(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_pharmacist),
):
    """Get sales within a date range. Requires pharmacist or admin role."""
    return sale_repository.get_by_date_range(db, start_date, end_date)


@router.get("/status/{status}", response_model=List[SaleRead])
def get_sales_by_status(
    status: str,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Get sales by status."""
    return sale_repository.get_by_status(db, status)


@router.post("/", response_model=SaleRead, status_code=status.HTTP_201_CREATED)
def create_sale(
    data: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new sale. Automatically assigns the current user as the cashier."""
    sale_data = data.model_dump()
    sale_data["user_id"] = current_user.id
    return sale_repository.create(db, sale_data)


@router.put("/{sale_id}", response_model=SaleRead)
def update_sale(
    sale_id: UUID,
    data: SaleUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    """Update an existing sale. Requires admin role."""
    sale = sale_repository.get(db, sale_id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    return sale_repository.update(db, sale, data.model_dump(exclude_unset=True))


@router.patch("/{sale_id}/status", response_model=SaleRead)
def update_sale_status(
    sale_id: UUID,
    status: str,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_pharmacist),
):
    """Update sale status. Requires pharmacist or admin role."""
    sale = sale_repository.update_status(db, sale_id, status)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    return sale


@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(
    sale_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    """Delete a sale. Requires admin role."""
    sale = sale_repository.get(db, sale_id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    sale_repository.delete(db, sale)
    return None