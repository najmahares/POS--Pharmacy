from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from app.models.product import Product

class ProductRepository:
    def __init__(self):
        self.model = Product

    def get(self, db: Session, id: UUID) -> Optional[Product]:
        return db.get(Product, id)
    
    def get_by_sku(self, db: Session, sku: str) -> Optional[Product]:
        return db.query(Product).filter(Product.sku == sku).first()
    
    def get_by_barcode(self, db: Session, barcode: str) -> Optional[Product]:
        return db.query(Product).filter(Product.barcode == barcode).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        return db.query(Product).offset(skip).limit(limit).all()
    
    def get_by_category(self, db: Session, category_id: UUID) -> List[Product]:
        return db.query(Product).filter(Product.category_id == category_id).all()
    
    def get_by_supplier(self, db: Session, supplier_id: UUID) -> List[Product]:
        return db.query(Product).filter(Product.supplier_id == supplier_id).all()
    
    def get_low_stock(self, db: Session) -> List[Product]:
        return db.query(Product).filter(
            Product.quantity_in_stock <= Product.reorder_level
        ).all()
    
    def get_expired_products(self, db: Session) -> List[Product]:
        from datetime import date
        return db.query(Product).filter(Product.expiry_date < date.today()).all()

    def create(self, db: Session, data: dict) -> Product:
        obj = Product(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: Product, data: dict) -> Product:
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Product) -> None:
        db.delete(db_obj)
        db.commit()
    
    def update_stock(self, db: Session, product_id: UUID, quantity: int) -> Product:
        product = self.get(db, product_id)
        if product:
            product.quantity_in_stock = quantity
            db.commit()
            db.refresh(product)
        return product

product_repository = ProductRepository()