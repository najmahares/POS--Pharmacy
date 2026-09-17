from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from app.models.payment import Payment

class PaymentRepository:
    def __init__(self):
        self.model = Payment

    def get(self, db: Session, id: UUID) -> Optional[Payment]:
        return db.get(Payment, id)

    def get_by_sale_id(self, db: Session, sale_id: UUID) -> List[Payment]:
        return db.query(Payment).filter(Payment.sale_id == sale_id).all()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Payment]:
        return db.query(Payment).offset(skip).limit(limit).all()

    def create(self, db: Session, data: dict) -> Payment:
        obj = Payment(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: Payment, data: dict) -> Payment:
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Payment) -> None:
        db.delete(db_obj)
        db.commit()

payment_repository = PaymentRepository()