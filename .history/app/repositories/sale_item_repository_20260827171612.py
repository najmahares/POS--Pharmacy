from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from app.models.sale_item import SaleItem

class SaleItemRepository:
    def __init__(self):
        self.model = SaleItem

    def get(self, db: Session, id: UUID) -> Optional[SaleItem]:
        return db.get(SaleItem, id)

    def get_by_sale_id(self, db: Session, sale_id: UUID) -> List[SaleItem]:
        return db.query(SaleItem).filter(SaleItem.sale_id == sale_id).all()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[SaleItem]:
        return db.query(SaleItem).offset(skip).limit(limit).all()

    def create(self, db: Session, data: dict) -> SaleItem:
        obj = SaleItem(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: SaleItem, data: dict) -> SaleItem:
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: SaleItem) -> None:
        db.delete(db_obj)
        db.commit()

sale_item_repository = SaleItemRepository()