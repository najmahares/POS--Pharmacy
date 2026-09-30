"""Customer schema module."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CustomerBase(BaseModel):
    """Base customer schema."""

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: str | None = Field(None, max_length=150)
    phone: str | None = Field(None, max_length=20)
    address: str | None = None
    date_of_birth: datetime | None = None
    medical_record_number: str | None = Field(None, max_length=50)
    insurance_provider: str | None = Field(None, max_length=100)
    insurance_policy_number: str | None = Field(None, max_length=50)
    is_active: bool = True


class CustomerCreate(CustomerBase):
    """Customer creation schema."""


class CustomerUpdate(BaseModel):
    """Customer update schema."""

    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    email: str | None = Field(None, max_length=150)
    phone: str | None = Field(None, max_length=20)
    address: str | None = None
    date_of_birth: datetime | None = None
    medical_record_number: str | None = Field(None, max_length=50)
    insurance_provider: str | None = Field(None, max_length=100)
    insurance_policy_number: str | None = Field(None, max_length=50)
    is_active: bool | None = None


class CustomerRead(CustomerBase):
    """Customer read schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
