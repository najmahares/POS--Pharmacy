from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from app.models.customer import Customer

class CustomerRepository:
    def __init__(self):
        self.model = Customer

    def get(self, db: Session, id: UUID) -> Optional[Customer]:
        return db.get(Customer, id)
    
    def get_by_medical_record(self, db: Session, medical_record_number: str) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.medical_record_number == medical_record_number).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Customer]:
        return db.query(Customer).offset(skip).limit(limit).all()

    def create(self, db: Session, data: dict) -> Customer:
        obj = Customer(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: Customer, data: dict) -> Customer:
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Customer) -> None:
        db.delete(db_obj)
        db.commit()

customer_repository = CustomerRepository()