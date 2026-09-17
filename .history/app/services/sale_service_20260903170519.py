
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.sale_repository import sale_repository
from app.schemas.sale import SaleCreate, SaleUpdate


def get_sale(db: Session, sale_id: UUID):
    """Get a sale by ID."""
    sale = sale_repository.get(db, sale_id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    return sale


def list_sales(db: Session):
    """List all sales."""
    return sale_repository.get_all(db)


def create_sale(db: Session, data: SaleCreate):
    """Create a new sale."""
    return sale_repository.create(db, data.model_dump())


def update_sale(db: Session, sale_id: UUID, data: SaleUpdate):
    """Update an existing sale."""
    sale = get_sale(db, sale_id)
    return sale_repository.update(db, sale, data.model_dump(exclude_unset=True))


def delete_sale(db: Session, sale_id: UUID):
    """Delete a sale."""
    sale = get_sale(db, sale_id)
    sale_repository.delete(db, sale)