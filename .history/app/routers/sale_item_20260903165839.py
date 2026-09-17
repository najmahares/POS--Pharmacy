from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_pharmacist
from app.repositories.sale_item_repository import sale_item_repository
from app.schemas.sale_item import SaleItemCreate, SaleItemRead, SaleItemUpdate

router = APIRouter()

@router.get("/", response_model=List[SaleItemRead])
def get_sale_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return sale_item_repository.get_all(db, skip, limit)

@router.post("/", response_model=SaleItemRead, status_code=status.HTTP_201_CREATED)
def create_sale_item(data: SaleItemCreate, db: Session = Depends(get_db), current_user: dict = Depends(require_pharmacist)):
    return sale_item_repository.create(db, data.model_dump())

@router.get("/{sale_item_id}", response_model=SaleItemRead)
def get_sale_item(sale_item_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    sale_item = sale_item_repository.get(db, sale_item_id)
    if not sale_item:
        raise HTTPException(status_code=404, detail="Sale item not found")
    return sale_item

@router.put("/{sale_item_id}", response_model=SaleItemRead)
def update_sale_item(sale_item_id: UUID, data: SaleItemUpdate, db: Session = Depends(get_db), current_user: dict = Depends(require_pharmacist)):
    sale_item = sale_item_repository.get(db, sale_item_id)
    if not sale_item:
        raise HTTPException(status_code=404, detail="Sale item not found")
    return sale_item_repository.update(db, sale_item, data.model_dump(exclude_unset=True))

@router.delete("/{sale_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale_item(sale_item_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    sale_item = sale_item_repository.get(db, sale_item_id)
    if not sale_item:
        raise HTTPException(status_code=404, detail="Sale item not found")
    sale_item_repository.delete(db, sale_item)
