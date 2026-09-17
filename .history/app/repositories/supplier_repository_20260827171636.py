from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from app.models.supplier import Supplier

class SupplierRepository:
    def __init__(self):
        self.model = Supplier

    def get(self, db: Session, id: UUID) -> Optional[Supplier]:
        return db.get(Supplier, id)

    def get_by_tax_id(self, db: Session, tax_id: str) -> Optional[Supplier]:
        return db.query(Supplier).filter(Supplier.tax_id == tax_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Supplier]:
        return db.query(Supplier).offset(skip).limit(limit).all()

    def create(self, db: Session, data: dict) -> Supplier:
        obj = Supplier(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: Supplier, data: dict) -> Supplier:
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Supplier) -> None:
        db.delete(db_obj)
        db.commit()

supplier_repository = SupplierRepository()