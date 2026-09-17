

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    """Repository class for Category model operations."""

    def __init__(self):
        """Initialize CategoryRepository."""
        self.model = Category

    def get(self, db: Session, category_id: UUID) -> Optional[Category]:
        """Get a category by UUID."""
        return db.get(Category, category_id)

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
        """Get all categories with pagination."""
        return db.query(Category).offset(skip).limit(limit).all()

    def get_by_name(self, db: Session, name: str) -> Optional[Category]:
        """Get a category by name (case-insensitive)."""
        return db.query(Category).filter(Category.name.ilike(name)).first()

    def get_root_categories(self, db: Session) -> List[Category]:
        """Get all root categories (categories with no parent)."""
        return db.query(Category).filter(Category.parent_id.is_(None)).all()

    def get_subcategories(self, db: Session, parent_id: UUID) -> List[Category]:
        """Get all subcategories of a parent category."""
        return db.query(Category).filter(Category.parent_id == parent_id).all()

    def create(self, db: Session, data: dict) -> Category:
        """Create a new category."""
        obj = Category(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: Category, data: dict) -> Category:
        """Update an existing category."""
        for field, value in data.items():
            if value is not None:
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Category) -> None:
        """Delete a category."""
        db.delete(db_obj)
        db.commit()


category_repository = CategoryRepository()

