import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    sku = Column(String, unique=True, index=True, nullable=False)
    barcode = Column(String, unique=True, index=True, nullable=True)
    description = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=False, default=Decimal('0.00'))
    cost = Column(Numeric(10, 2), nullable=False, default=Decimal('0.00'))
    quantity_in_stock = Column(Integer, default=0)
    reorder_level = Column(Integer, default=0)
    expiry_date = Column(DateTime, nullable=True)

    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    sale_items = relationship("SaleItem", back_populates="product")

