
from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:
    """Repository class for Product model operations."""

    def __init__(self):
        """Initialize ProductRepository."""
        self.model = Product

    def get(self, db: Session, product_id: UUID) -> Optional[Product]:
        """Get a product by UUID."""
        return db.get(Product, product_id)

    def get_by_sku(self, db: Session, sku: str) -> Optional[Product]:
        """Get a product by SKU."""
        return db.query(Product).filter(Product.sku == sku).first()

    def get_by_barcode(self, db: Session, barcode: str) -> Optional[Product]:
        """Get a product by barcode."""
        return db.query(Product).filter(Product.barcode == barcode).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get all products with pagination."""
        return db.query(Product).offset(skip).limit(limit).all()

    def get_by_category(self, db: Session, category_id: UUID) -> List[Product]:
        """Get all products in a category."""
        return db.query(Product).filter(Product.category_id == category_id).all()

    def get_by_supplier(self, db: Session, supplier_id: UUID) -> List[Product]:
        """Get all products from a supplier."""
        return db.query(Product).filter(Product.supplier_id == supplier_id).all()

    def get_low_stock(self, db: Session) -> List[Product]:
        """Get products with low stock (quantity <= reorder_level)."""
        return db.query(Product).filter(
            Product.quantity_in_stock <= Product.reorder_level
        ).all()

    def get_expired_products(self, db: Session) -> List[Product]:
        """Get expired products."""
        return db.query(Product).filter(Product.expiry_date < date.today()).all()

    def create(self, db: Session, data: dict) -> Product:
        """Create a new product."""
        obj = Product(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: Product, data: dict) -> Product:
        """Update an existing product."""
        for field, value in data.items():
            if value is not None:
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Product) -> None:
        """Delete a product."""
        db.delete(db_obj)
        db.commit()

    def update_stock(self, db: Session, product_id: UUID, quantity: int) -> Product:
        """Update product stock quantity."""
        product = self.get(db, product_id)
        if product:
            product.quantity_in_stock = quantity
            db.commit()
            db.refresh(product)
        return product


product_repository = ProductRepository()

