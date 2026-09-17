from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.repositories.category_repository import category_repository
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter()

@router.get("/", response_model=List[CategoryRead])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return category_repository.get_all(db, skip, limit)

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    return category_repository.create(db, data.model_dump())

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    category = category_repository.get(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: UUID, data: CategoryUpdate, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    category = category_repository.get(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category_repository.update(db, category, data.model_dump(exclude_unset=True))

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    category = category_repository.get(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category_repository.delete(db, category)
