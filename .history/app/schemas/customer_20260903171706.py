"""Customer schema module."""

from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CustomerBase(BaseModel):
    """Base customer schema."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: Optional[str] = Field(None, max_length=150)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    medical_record_number: Optional[str] = Field(None, max_length=50)
    insurance_provider: Optional[str] = Field(None, max_length=100)
    insurance_policy_number: Optional[str] = Field(None, max_length=50)
    is_active: bool = True


class CustomerCreate(CustomerBase):
    """Customer creation schema."""
    pass


class CustomerUpdate(BaseModel):
    """Customer update schema."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, max_length=150)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    medical_record_number: Optional[str] = Field(None, max_length=50)
    insurance_provider: Optional[str] = Field(None, max_length=100)
    insurance_policy_number: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class CustomerRead(CustomerBase):
    """Customer read schema."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime