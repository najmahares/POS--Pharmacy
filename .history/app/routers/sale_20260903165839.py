from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_pharmacist
from app.repositories.sale_repository import sale_repository
from app.schemas.sale import SaleCreate, SaleRead, SaleUpdate

router = APIRouter()

@router.get("/", response_model=List[SaleRead])
def get_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return sale_repository.get_all(db, skip, limit)

@router.post("/", response_model=SaleRead, status_code=status.HTTP_201_CREATED)
def create_sale(data: SaleCreate, db: Session = Depends(get_db), current_user: dict = Depends(require_pharmacist)):
    return sale_repository.create(db, data.model_dump())

@router.get("/{sale_id}", response_model=SaleRead)
def get_sale(sale_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    sale = sale_repository.get(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale

@router.put("/{sale_id}", response_model=SaleRead)
def update_sale(sale_id: UUID, data: SaleUpdate, db: Session = Depends(get_db), current_user: dict = Depends(require_pharmacist)):
    sale = sale_repository.get(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale_repository.update(db, sale, data.model_dump(exclude_unset=True))

@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(sale_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    sale = sale_repository.get(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    sale_repository.delete(db, sale)
