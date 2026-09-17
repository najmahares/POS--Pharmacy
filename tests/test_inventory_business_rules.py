import uuid
from datetime import date, datetime, timedelta

import pytest


def _sale(client, headers, subtotal="10.00", tax="1.00", status="pending"):
    return client.post(
        "/sales/",
        json={
            "sale_number": f"SAL-{uuid.uuid4().hex[:8]}",
            "sale_date": datetime.utcnow().isoformat(),
            "subtotal": subtotal,
            "tax_amount": tax,
            "discount_amount": "0",
            "total_amount": f"{float(subtotal) + float(tax):.2f}",
            "status": status,
        },
        headers=headers,
    ).json()


def _item(sale_id, product_id, qty="1", unit="10.00"):
    return {
        "quantity": qty,
        "unit_price": unit,
        "discount_amount": "0",
        "tax_amount": "0",
        "total_price": f"{float(qty) * float(unit):.2f}",
        "sale_id": sale_id,
        "product_id": product_id,
    }


def test_sale_item_decrements_product_stock(client, auth_headers, product, db_session):
    before = product.quantity_in_stock
    sale = _sale(client, auth_headers)
    r = client.post(
        "/sale-items/",
        json=_item(sale["id"], str(product.id), qty="3"),
        headers=auth_headers,
    )
    assert r.status_code == 201
    db_session.refresh(product)
    assert product.quantity_in_stock == before - 3


def test_cannot_sell_more_than_stock(client, auth_headers, product, db_session):
    sale = _sale(client, auth_headers)
    r = client.post(
        "/sale-items/",
        json=_item(sale["id"], str(product.id), qty="999999"),
        headers=auth_headers,
    )
    assert r.status_code in (400, 409, 422)
    db_session.refresh(product)
    assert product.quantity_in_stock >= 0


def test_stock_never_goes_negative(client, auth_headers, product, db_session):
    for _ in range(5):
        sale = _sale(client, auth_headers)
        client.post(
            "/sale-items/",
            json=_item(sale["id"], str(product.id), qty="999999"),
            headers=auth_headers,
        )
    db_session.refresh(product)
    assert product.quantity_in_stock >= 0


def test_total_price_equals_quantity_times_unit(client, auth_headers, product):
    sale = _sale(client, auth_headers)
    payload = _item(sale["id"], str(product.id), qty="3", unit="9.99")
    r = client.post("/sale-items/", json=payload, headers=auth_headers)
    assert r.status_code == 201
    from decimal import Decimal
    assert Decimal(str(r.json()["total_price"])) == Decimal("29.97")


def test_fractional_quantity_for_liquids(client, auth_headers, product):
    sale = _sale(client, auth_headers)
    r = client.post(
        "/sale-items/",
        json=_item(sale["id"], str(product.id), qty="0.500", unit="12.00"),
        headers=auth_headers,
    )
    assert r.status_code == 201
    from decimal import Decimal
    assert Decimal(str(r.json()["quantity"])) == Decimal("0.5")


def test_negative_quantity_rejected(client, auth_headers, product):
    sale = _sale(client, auth_headers)
    r = client.post(
        "/sale-items/",
        json=_item(sale["id"], str(product.id), qty="-1"),
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_zero_quantity_rejected(client, auth_headers, product):
    sale = _sale(client, auth_headers)
    r = client.post(
        "/sale-items/",
        json=_item(sale["id"], str(product.id), qty="0"),
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_negative_price_rejected(client, auth_headers, product):
    sale = _sale(client, auth_headers)
    r = client.post(
        "/sale-items/",
        json=_item(sale["id"], str(product.id), unit="-5.00"),
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_rx_product_can_be_sold_with_prescription(client, auth_headers, rx_product):
    sale = client.post("/sales/", json={
        "sale_number": f"SAL-{uuid.uuid4().hex[:8]}",
        "sale_date": datetime.utcnow().isoformat(),
        "subtotal": "10.00", "tax_amount": "0",
        "discount_amount": "0", "total_amount": "10.00",
        "status": "pending",
        "prescription_number": "RX-12345",
        "prescribing_doctor": "Dr. Strange",
    }, headers=auth_headers).json()
    assert sale.get("prescription_number") == "RX-12345"
    r = client.post(
        "/sale-items/",
        json=_item(sale["id"], str(rx_product.id)),
        headers=auth_headers,
    )
    assert r.status_code == 201


def test_expired_product_listing(client, inventory_headers, db_session, category):
    from app.models.product import Product
    expired = Product(
        id=uuid.uuid4(),
        name="Old Aspirin",
        sku=f"OLD-{uuid.uuid4().hex[:6]}",
        price="5.00",
        cost="1.00",
        quantity_in_stock=10,
        reorder_level=1,
        expiry_date=date.today() - timedelta(days=1),
        category_id=category.id,
    )
    db_session.add(expired)
    db_session.commit()
    r = client.get("/products/expired", headers=inventory_headers)
    assert r.status_code == 200
    ids = [p["id"] for p in r.json()]
    assert str(expired.id) in ids


def test_low_stock_endpoint_returns_only_low(client, inventory_headers, db_session, category, product):
    from app.models.product import Product
    low = Product(
        id=uuid.uuid4(),
        name="Low Item",
        sku=f"LOW-{uuid.uuid4().hex[:6]}",
        price="5.00",
        cost="1.00",
        quantity_in_stock=1,
        reorder_level=10,
        expiry_date=date.today() + timedelta(days=30),
        category_id=category.id,
    )
    db_session.add(low)
    db_session.commit()
    r = client.get("/products/low-stock", headers=inventory_headers)
    assert r.status_code == 200
    ids = [p["id"] for p in r.json()]
    assert str(low.id) in ids
    assert str(product.id) not in ids
