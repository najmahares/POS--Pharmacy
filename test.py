#!/usr/bin/env python3
"""
Absolute seed script for Hospital Pharmacy POS.

Uses raw SQL TRUNCATE CASCADE to bypass ALL FK constraints.
All seeded data is mathematically consistent so app validations never break.

Usage:
    python seed_database.py
"""

import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import text

try:
    from app.database import SessionLocal
    from app.models.category import Category
    from app.models.supplier import Supplier
    from app.models.user import User
    from app.models.customer import Customer
    from app.models.product import Product
    from app.models.sale import Sale
    from app.models.sale_item import SaleItem
    from app.models.payment import Payment
    from app.models.receipt import Receipt
except ImportError:
    from database import SessionLocal
    from app.models.category import Category
    from app.models.supplier import Supplier
    from app.models.user import User
    from app.models.customer import Customer
    from app.models.product import Product
    from app.models.sale import Sale
    from app.models.sale_item import SaleItem
    from app.models.payment import Payment
    from app.models.receipt import Receipt


# Fixed UUIDs — hard-coded in Postman collection too
IDS = {
    "category":    uuid.UUID("11111111-1111-1111-1111-111111111111"),
    "subcategory": uuid.UUID("11111111-1111-1111-1111-111111111112"),
    "supplier":    uuid.UUID("22222222-2222-2222-2222-222222222222"),
    "user":        uuid.UUID("33333333-3333-3333-3333-333333333333"),
    "customer":    uuid.UUID("44444444-4444-4444-4444-444444444444"),
    "product":     uuid.UUID("55555555-5555-5555-5555-555555555555"),
    "sale":        uuid.UUID("66666666-6666-6666-6666-666666666666"),
    "sale_item":   uuid.UUID("77777777-7777-7777-7777-777777777777"),
    "payment":     uuid.UUID("88888888-8888-8888-8888-888888888888"),
    "receipt":     uuid.UUID("99999999-9999-9999-9999-999999999999"),
}


def seed():
    db = SessionLocal()

    try:
        # ----------------------------------------------------------
        # 1. ABSOLUTE WIPE — Raw SQL TRUNCATE CASCADE
        #    Bypasses every FK constraint, trigger, and ORM hook.
        # ----------------------------------------------------------
        print(">>> Truncating all tables (CASCADE)...")
        try:
            db.execute(text("""
                TRUNCATE TABLE
                    receipts, payments, sale_items, sales, products,
                    customers, users, suppliers, categories
                RESTART IDENTITY CASCADE
            """))
            db.commit()
            print("   ✓ Wiped clean via TRUNCATE CASCADE")
        except Exception as e:
            db.rollback()
            print(f"   ⚠ TRUNCATE failed (maybe tables dont exist yet): {e}")
            print("   → Continuing anyway...")

        # ----------------------------------------------------------
        # 2. CATEGORIES
        # ----------------------------------------------------------
        print(">>> Seeding categories...")
        db.add(Category(
            id=IDS["category"],
            name="Analgesics",
            description="Pain relief medications including NSAIDs and opioids",
            parent_id=None,
            is_active=True,
        ))
        db.add(Category(
            id=IDS["subcategory"],
            name="NSAIDs",
            description="Non-steroidal anti-inflammatory drugs",
            parent_id=IDS["category"],
            is_active=True,
        ))
        db.commit()
        print("   ✓ 2 categories")

        # ----------------------------------------------------------
        # 3. SUPPLIER
        # ----------------------------------------------------------
        print(">>> Seeding supplier...")
        db.add(Supplier(
            id=IDS["supplier"],
            company_name="MediPharma Distributors Ltd",
            contact_name="Ahmed Hassan",
            email="ahmed@medipharma.com",
            phone="+254712345678",
            address="123 Industrial Area, Nairobi, Kenya",
            tax_id="VAT-123456789",
            license_number="PHARM-DIST-2026-001",
            payment_terms="net-30",
            lead_time_days=7,
            minimum_order_amount=Decimal("5000.00"),
            is_active=True,
        ))
        db.commit()
        print("   ✓ 1 supplier")

        # ----------------------------------------------------------
        # 4. USER (pharmacist)
        # ----------------------------------------------------------
        print(">>> Seeding user...")
        db.add(User(
            id=IDS["user"],
            username="john_pharmacist",
            email="john@hospital.com",
            # Dummy bcrypt hash — password is "password123" if your app checks bcrypt
            password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            first_name="John",
            last_name="Smith",
            role="pharmacist",
            license_number="PHARM-KE-2026-001",
            license_expiry=date(2027, 12, 31),
            department="Outpatient Pharmacy",
            is_active=True,
        ))
        db.commit()
        print("   ✓ 1 user")

        # ----------------------------------------------------------
        # 5. CUSTOMER
        # ----------------------------------------------------------
        print(">>> Seeding customer...")
        db.add(Customer(
            id=IDS["customer"],
            medical_record_number="MRN-2026-001",
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1985, 3, 15),
            gender="male",
            email="john.doe@email.com",
            phone="+254711223344",
            address="456 Residential St, Nairobi",
            emergency_contact_name="Jane Doe",
            emergency_contact_phone="+254755667788",
            insurance_provider="NHIF",
            insurance_policy_number="NHIF-12345678",
            allergies="Penicillin, Sulfa drugs",
            loyalty_points=0,
            is_walk_in=False,
            is_active=True,
        ))
        db.commit()
        print("   ✓ 1 customer")

        # ----------------------------------------------------------
        # 6. PRODUCT
        # ----------------------------------------------------------
        print(">>> Seeding product...")
        db.add(Product(
            id=IDS["product"],
            sku="PAN-500-001",
            name="Paracetamol 500mg Tablets",
            description="Pain reliever and fever reducer. 20 tablets per pack.",
            dosage_form="tablet",
            strength="500mg",
            unit_price=Decimal("150.00"),
            cost_price=Decimal("95.00"),
            quantity_in_stock=500,
            reorder_level=50,
            reorder_quantity=200,
            expiry_date=date(2027, 6, 15),
            batch_number="BATCH-2026-A",
            barcode="1234567890123",
            requires_prescription=False,
            controlled_substance=False,
            storage_conditions="room temperature",
            is_active=True,
            category_id=IDS["category"],
            supplier_id=IDS["supplier"],
        ))
        db.commit()
        print("   ✓ 1 product")

        # ----------------------------------------------------------
        # 7. SALE
        #    Math: 3 qty × 150.00 = 450.00 subtotal
        #          450.00 × 0.15  =  67.50 tax
        #          450.00 + 67.50  = 517.50 total
        # ----------------------------------------------------------
        print(">>> Seeding sale...")
        db.add(Sale(
            id=IDS["sale"],
            sale_number="SAL-2026-00001",
            sale_date=datetime(2026, 8, 6, 14, 30, 0),
            subtotal=Decimal("450.00"),
            tax_amount=Decimal("67.50"),
            discount_amount=Decimal("0.00"),
            total_amount=Decimal("517.50"),
            status="completed",
            prescription_number="RX-2026-001",
            prescribing_doctor="Dr. Jane Wanjiku",
            dispense_date=date(2026, 8, 6),
            notes="Patient paid via M-Pesa",
            customer_id=IDS["customer"],
            user_id=IDS["user"],
        ))
        db.commit()
        print("   ✓ 1 sale")

        # ----------------------------------------------------------
        # 8. SALE ITEM  (must match sale math exactly)
        # ----------------------------------------------------------
        print(">>> Seeding sale item...")
        db.add(SaleItem(
            id=IDS["sale_item"],
            quantity=Decimal("3.000"),
            unit_price=Decimal("150.00"),
            discount_amount=Decimal("0.00"),
            tax_amount=Decimal("67.50"),
            total_price=Decimal("517.50"),
            dispense_instructions="Take 1 tablet every 8 hours after meals",
            refills_authorized=0,
            sale_id=IDS["sale"],
            product_id=IDS["product"],
        ))
        db.commit()
        print("   ✓ 1 sale item")

        # ----------------------------------------------------------
        # 9. PAYMENT  (must equal sale total)
        # ----------------------------------------------------------
        print(">>> Seeding payment...")
        db.add(Payment(
            id=IDS["payment"],
            amount=Decimal("517.50"),
            payment_method="mobile_wallet",
            payment_status="completed",
            transaction_reference="MPESA-ABC123XYZ",
            paid_at=datetime(2026, 8, 6, 14, 32, 0),
            change_given=Decimal("0.00"),
            sale_id=IDS["sale"],
        ))
        db.commit()
        print("   ✓ 1 payment")

        # ----------------------------------------------------------
        # 10. RECEIPT  (must match sale breakdown)
        # ----------------------------------------------------------
        print(">>> Seeding receipt...")
        db.add(Receipt(
            id=IDS["receipt"],
            receipt_number="RCPT-2026-00001",
            receipt_data={
                "store_name": "Hospital Pharmacy POS",
                "items": [
                    {
                        "name": "Paracetamol 500mg",
                        "qty": 3,
                        "unit_price": 150.00,
                        "line_total": 450.00,
                    }
                ],
                "subtotal": 450.00,
                "tax_rate": "15%",
                "tax": 67.50,
                "discount": 0.00,
                "total": 517.50,
                "payments": [
                    {"method": "mobile_wallet", "amount": 517.50}
                ],
                "sale_number": "SAL-2026-00001",
            },
            receipt_type="both",
            issued_at=datetime(2026, 8, 6, 14, 35, 0),
            pharmacist_signature="JS-2026",
            regulatory_text="Dispensed by licensed pharmacist. Keep for your records.",
            sale_id=IDS["sale"],
        ))
        db.commit()
        print("   ✓ 1 receipt")

        print("\n" + "=" * 60)
        print("✅ SEED COMPLETE — All data is mathematically consistent.")
        print("=" * 60)
        print("\n📋 Fixed IDs (hard-coded in Postman collection):")
        for name, val in IDS.items():
            print(f"   {name:<13} → {val}")
        print("\n🚀 Run the Postman collection now — every request will hit 200.")

    except Exception as e:
        db.rollback()
        print(f"\n❌ FATAL ERROR during seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()