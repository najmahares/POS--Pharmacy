from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    sku: str = Field(..., min_length=1, max_length=50)
    barcode: str | None = Field(None, max_length=50)
    description: str | None = None
    price: Decimal = Field(..., ge=0)
    cost: Decimal = Field(0, ge=0)
    quantity_in_stock: int = Field(0, ge=0)
    reorder_level: int = Field(0, ge=0)
    expiry_date: date | None = None
    category_id: UUID | None = None
    supplier_id: UUID | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    sku: str | None = Field(None, min_length=1, max_length=50)
    barcode: str | None = Field(None, max_length=50)
    description: str | None = None
    price: Decimal | None = Field(None, ge=0)
    cost: Decimal | None = Field(None, ge=0)
    quantity_in_stock: int | None = Field(None, ge=0)
    reorder_level: int | None = Field(None, ge=0)
    expiry_date: date | None = None
    category_id: UUID | None = None
    supplier_id: UUID | None = None


class ProductResponse(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


ProductRead = ProductResponse
