from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_inventory_manager
from app.repositories.product_repository import product_repository
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate

router = APIRouter()

@router.get("/", response_model=List[ProductRead])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return product_repository.get_all(db, skip, limit)

@router.get("/low-stock", response_model=List[ProductRead])
def get_low_stock_products(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return product_repository.get_low_stock(db)

@router.get("/expired", response_model=List[ProductRead])
def get_expired_products(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return product_repository.get_expired_products(db)

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, db: Session = Depends(get_db), current_user: dict = Depends(require_inventory_manager)):
    return product_repository.create(db, data.model_dump())

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    product = product_repository.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: UUID, data: ProductUpdate, db: Session = Depends(get_db), current_user: dict = Depends(require_inventory_manager)):
    product = product_repository.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_repository.update(db, product, data.model_dump(exclude_unset=True))

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(require_inventory_manager)):
    product = product_repository.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_repository.delete(db, product)
