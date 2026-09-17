from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models.user import User
from app.models.product import Product
from app.repositories.sale_item_repository import sale_item_repository
from app.schemas.sale_item import SaleItemCreate, SaleItemRead, SaleItemUpdate

router = APIRouter(prefix="/sale-items", tags=["sale_items"])

@router.get("/", response_model=List[SaleItemRead])
def get_sale_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return sale_item_repository.get_all(db, skip=skip, limit=limit)

@router.get("/{sale_item_id}", response_model=SaleItemRead)
def get_sale_item(
    sale_item_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    sale_item = sale_item_repository.get(db, sale_item_id)
    if not sale_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale item not found"
        )
    return sale_item

@router.get("/sale/{sale_id}", response_model=List[SaleItemRead])
def get_sale_items_by_sale(
    sale_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return sale_item_repository.get_by_sale(db, sale_id)

@router.get("/product/{product_id}", response_model=List[SaleItemRead])
def get_sale_items_by_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return sale_item_repository.get_by_product(db, product_id)

@router.post("/", response_model=SaleItemRead, status_code=status.HTTP_201_CREATED)
def create_sale_item(
    data: SaleItemCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Create a sale item and atomically decrement product stock."""
    qty = Decimal(str(data.quantity))
    if qty <= 0:
        raise HTTPException(status_code=422, detail="Quantity must be greater than zero")

    product = db.get(Product, data.product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.quantity_in_stock is None or product.quantity_in_stock < qty:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient stock: available {product.quantity_in_stock}, requested {qty}",
        )

    product.quantity_in_stock = product.quantity_in_stock - qty
    try:
        item = sale_item_repository.create(db, data.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid sale_id or product_id")
    return item


@router.post("/bulk", response_model=List[SaleItemRead], status_code=status.HTTP_201_CREATED)
def create_sale_items_bulk(
    items: List[SaleItemCreate],
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    items_data = [item.model_dump() for item in items]
    return sale_item_repository.create_bulk(db, items_data)

@router.put("/{sale_item_id}", response_model=SaleItemRead)
def update_sale_item(
    sale_item_id: UUID,
    data: SaleItemUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    sale_item = sale_item_repository.get(db, sale_item_id)
    if not sale_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale item not found"
        )
    return sale_item_repository.update(db, sale_item, data.model_dump(exclude_unset=True))

@router.delete("/{sale_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale_item(
    sale_item_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    sale_item = sale_item_repository.get(db, sale_item_id)
    if not sale_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale item not found"
        )
    sale_item_repository.delete(db, sale_item)
    return None