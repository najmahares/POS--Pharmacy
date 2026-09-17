from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from app.models.sale import Sale

class SaleRepository:
    def __init__(self):
        self.model = Sale

    def get(self, db: Session, id: UUID) -> Optional[Sale]:
        return db.get(Sale, id)

    def get_by_sale_number(self, db: Session, sale_number: str) -> Optional[Sale]:
        return db.query(Sale).filter(Sale.sale_number == sale_number).first()

    def get_by_prescription_number(self, db: Session, prescription_number: str) -> Optional[Sale]:
        return db.query(Sale).filter(Sale.prescription_number == prescription_number).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Sale]:
        return db.query(Sale).offset(skip).limit(limit).all()

    def create(self, db: Session, data: dict) -> Sale:
        obj = Sale(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: Sale, data: dict) -> Sale:
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Sale) -> None:
        db.delete(db_obj)
        db.commit()

sale_repository = SaleRepository()