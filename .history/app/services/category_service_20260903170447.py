
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.category_repository import category_repository
from app.schemas.category import CategoryCreate, CategoryUpdate


def get_category(db: Session, category_id: UUID):
    """Get a category by ID."""
    category = category_repository.get(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


def list_categories(db: Session):
    """List all categories."""
    return category_repository.get_all(db)


def create_category(db: Session, data: CategoryCreate):
    """Create a new category."""
    return category_repository.create(db, data.model_dump())


def update_category(db: Session, category_id: UUID, data: CategoryUpdate):
    """Update an existing category."""
    category = get_category(db, category_id)
    return category_repository.update(db, category, data.model_dump(exclude_unset=True))


def delete_category(db: Session, category_id: UUID):
    """Delete a category."""
    category = get_category(db, category_id)
    category_repository.delete(db, category)