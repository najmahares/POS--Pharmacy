from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    sku: str = Field(..., min_length=1, max_length=50)
    barcode: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    price: Decimal = Field(..., ge=0)
    cost: Decimal = Field(0, ge=0)
    quantity_in_stock: int = Field(0, ge=0)
    reorder_level: int = Field(0, ge=0)
    expiry_date: Optional[datetime] = None
    category_id: Optional[UUID] = None
    supplier_id: Optional[UUID] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    sku: Optional[str] = Field(None, min_length=1, max_length=50)
    barcode: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    cost: Optional[Decimal] = Field(None, ge=0)
    quantity_in_stock: Optional[int] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)
    expiry_date: Optional[datetime] = None
    category_id: Optional[UUID] = None
    supplier_id: Optional[UUID] = None


class ProductResponse(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


ProductRead = ProductResponse
