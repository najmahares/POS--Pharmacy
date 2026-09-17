
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.product_repository import product_repository
from app.schemas.product import ProductCreate, ProductUpdate


def get_product(db: Session, product_id: UUID):
    """Get a product by ID."""
    product = product_repository.get(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


def list_products(db: Session):
    """List all products."""
    return product_repository.get_all(db)


def create_product(db: Session, data: ProductCreate):
    """Create a new product."""
    return product_repository.create(db, data.model_dump())


def update_product(db: Session, product_id: UUID, data: ProductUpdate):
    """Update an existing product."""
    product = get_product(db, product_id)
    return product_repository.update(db, product, data.model_dump(exclude_unset=True))


def delete_product(db: Session, product_id: UUID):
    """Delete a product."""
    product = get_product(db, product_id)
    product_repository.delete(db, product)
