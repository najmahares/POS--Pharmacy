"""Product schema module."""

from datetime import datetime, date
from uuid import UUID
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    """Base product schema."""
    name: str = Field(..., min_length=1, max_length=200)
    sku: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    unit_price: Decimal = Field(..., ge=0)
    cost_price: Optional[Decimal] = Field(None, ge=0)
    quantity_in_stock: int = Field(..., ge=0)
    reorder_level: int = Field(..., ge=0)
    reorder_quantity: Optional[int] = Field(None, ge=0)
    expiry_date: date
    batch_number: Optional[str] = Field(None, max_length=50)
    barcode: Optional[str] = Field(None, max_length=50)
    requires_prescription: bool = False
    controlled_substance: bool = False
    storage_conditions: Optional[str] = Field(None, max_length=100)
    is_active: bool = True
    category_id: UUID
    supplier_id: Optional[UUID] = None


class ProductCreate(ProductBase):
    """Product creation schema."""
    pass


class ProductUpdate(BaseModel):

    """Product update schema."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    sku: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    unit_price: Optional[Decimal] = Field(None, ge=0)
    cost_price: Optional[Decimal] = Field(None, ge=0)
    quantity_in_stock: Optional[int] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)
    reorder_quantity: Optional[int] = Field(None, ge=0)
    expiry_date: Optional[date] = None
    batch_number: Optional[str] = Field(None, max_length=50)
    barcode: Optional[str] = Field(None, max_length=50)
    requires_prescription: Optional[bool] = None
    controlled_substance: Optional[bool] = None
    storage_conditions: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None
    category_id: Optional[UUID] = None
    supplier_id: Optional[UUID] = None


class ProductRead(ProductBase):
    """Product read schema."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime