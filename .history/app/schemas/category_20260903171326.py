from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[UUID] = None
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime

