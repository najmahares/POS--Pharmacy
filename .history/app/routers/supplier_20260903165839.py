from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.repositories.supplier_repository import supplier_repository
from app.schemas.supplier import SupplierCreate, SupplierRead, SupplierUpdate

router = APIRouter()

@router.get("/", response_model=List[SupplierRead])
def get_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return supplier_repository.get_all(db, skip, limit)

@router.post("/", response_model=SupplierRead, status_code=status.HTTP_201_CREATED)
def create_supplier(data: SupplierCreate, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    return supplier_repository.create(db, data.model_dump())

@router.get("/{supplier_id}", response_model=SupplierRead)
def get_supplier(supplier_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    supplier = supplier_repository.get(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.put("/{supplier_id}", response_model=SupplierRead)
def update_supplier(supplier_id: UUID, data: SupplierUpdate, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    supplier = supplier_repository.get(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier_repository.update(db, supplier, data.model_dump(exclude_unset=True))

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    supplier = supplier_repository.get(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    supplier_repository.delete(db, supplier)
