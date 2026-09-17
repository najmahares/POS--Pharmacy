from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from app.models.receipt import Receipt

class ReceiptRepository:
    def __init__(self):
        self.model = Receipt

    def get(self, db: Session, id: UUID) -> Optional[Receipt]:
        return db.get(Receipt, id)

    def get_by_receipt_number(self, db: Session, receipt_number: str) -> Optional[Receipt]:
        return db.query(Receipt).filter(Receipt.receipt_number == receipt_number).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Receipt]:
        return db.query(Receipt).offset(skip).limit(limit).all()

    def create(self, db: Session, data: dict) -> Receipt:
        obj = Receipt(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: Receipt, data: dict) -> Receipt:
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Receipt) -> None:
        db.delete(db_obj)
        db.commit()

receipt_repository = ReceiptRepository()