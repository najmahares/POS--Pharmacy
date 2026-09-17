from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from app.models.category import Category

class CategoryRepository:
    def __init__(self):
        self.model = Category

    def get(self, db: Session, id: UUID) -> Optional[Category]:
        return db.get(Category, id)

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
        return db.query(Category).offset(skip).limit(limit).all()

    def create(self, db: Session, data: dict) -> Category:
        obj = Category(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: Category, data: dict) -> Category:
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Category) -> None:
        db.delete(db_obj)
        db.commit()

category_repository = CategoryRepository()