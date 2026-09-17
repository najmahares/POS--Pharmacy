
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.sale_item import SaleItem


class SaleItemRepository:
    """Repository class for SaleItem model operations."""

    def __init__(self):
        """Initialize SaleItemRepository."""
        self.model = SaleItem

    def get(self, db: Session, sale_item_id: UUID) -> Optional[SaleItem]:
        """Get a sale item by UUID."""
        return db.get(SaleItem, sale_item_id)

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[SaleItem]:
        """Get all sale items with pagination."""
        return db.query(SaleItem).offset(skip).limit(limit).all()

    def get_by_sale(self, db: Session, sale_id: UUID) -> List[SaleItem]:
        """Get all items in a sale."""
        return db.query(SaleItem).filter(SaleItem.sale_id == sale_id).all()

    def get_by_product(self, db: Session, product_id: UUID) -> List[SaleItem]:
        """Get all sale items for a product."""
        return db.query(SaleItem).filter(SaleItem.product_id == product_id).all()

    def create(self, db: Session, data: dict) -> SaleItem:
        """Create a new sale item."""
        obj = SaleItem(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def create_bulk(self, db: Session, items_data: list) -> List[SaleItem]:
        """Create multiple sale items at once."""
        items = [SaleItem(**data) for data in items_data]
        db.add_all(items)
        db.commit()
        for item in items:
            db.refresh(item)
        return items

    def update(self, db: Session, db_obj: SaleItem, data: dict) -> SaleItem:
        """Update an existing sale item."""
        for field, value in data.items():
            if value is not None:
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: SaleItem) -> None:
        """Delete a sale item."""
        db.delete(db_obj)
        db.commit()


sale_item_repository = SaleItemRepository()

