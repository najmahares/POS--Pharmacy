from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    sku: str
    barcode: Optional[str] = None
    description: Optional[str] = None
    price: Decimal
    cost: Decimal
    quantity_in_stock: int = 0
    reorder_level: int = 0
    expiry_date: Optional[datetime] = None
    category_id: Optional[UUID] = None
    supplier_id: Optional[UUID] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    cost: Optional[Decimal] = None
    quantity_in_stock: Optional[int] = None
    reorder_level: Optional[int] = None
    expiry_date: Optional[datetime] = None
    category_id: Optional[UUID] = None
    supplier_id: Optional[UUID] = None


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime

