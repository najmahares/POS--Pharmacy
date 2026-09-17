from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin, require_inventory_manager
from app.models.user import User
from app.repositories.category_repository import category_repository
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[CategoryRead])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return category_repository.get_all(db, skip, limit)

@router.get("/root", response_model=List[CategoryRead])
def get_root_categories(
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return category_repository.get_root_categories(db)

@router.get("/{category_id}/subcategories", response_model=List[CategoryRead])
def get_subcategories(
    category_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    category = category_repository.get(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category_repository.get_subcategories(db, category_id)

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    category = category_repository.get(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_inventory_manager),
):
    existing = category_repository.get_by_name(db, data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name '{data.name}' already exists"
        )
    if data.parent_id:
        parent = category_repository.get(db, data.parent_id)
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent category not found"
            )
    return category_repository.create(db, data.model_dump())

@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_inventory_manager),
):
    category = category_repository.get(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    if data.name:
        existing = category_repository.get_by_name(db, data.name)
        if existing and existing.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name '{data.name}' already exists"
            )
    if data.parent_id:
        if data.parent_id == category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category cannot be its own parent"
            )
        parent = category_repository.get(db, data.parent_id)
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent category not found"
            )
    return category_repository.update(db, category, data.model_dump(exclude_unset=True))

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    category = category_repository.get(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    if category.products:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete category with {len(category.products)} associated products"
        )
    subcategories = category_repository.get_subcategories(db, category_id)
    if subcategories:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete category with {len(subcategories)} subcategories"
        )
    category_repository.delete(db, category)
    return None