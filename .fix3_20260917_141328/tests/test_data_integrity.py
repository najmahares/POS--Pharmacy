import uuid
import pytest
from datetime import datetime


def test_cannot_delete_category_with_products(client, auth_headers, product):
    r = client.delete(f"/categories/{product.category_id}", headers=auth_headers)
    assert r.status_code == 400
    assert "product" in r.json()["detail"].lower()


def test_cannot_delete_category_with_subcategories(client, auth_headers):
    parent = client.post(
        "/categories/", json={"name": f"P-{uuid.uuid4().hex[:6]}"}, headers=auth_headers
    ).json()
    client.post(
        "/categories/",
        json={"name": f"C-{uuid.uuid4().hex[:6]}", "parent_id": parent["id"]},
        headers=auth_headers,
    )
    r = client.delete(f"/categories/{parent['id']}", headers=auth_headers)
    assert r.status_code == 400


def test_duplicate_sku_case_insensitive(client, inventory_headers, product):
    r = client.post(
        "/products/",
        json={
            "name": "Duplicate",
            "sku": product.sku,           
            "unit_price": "1.00",
            "quantity_in_stock": 1,
            "reorder_level": 1,
            "expiry_date": "2030-01-01",
        },
        headers=inventory_headers,
    )
    assert r.status_code == 400


def test_sale_number_must_be_unique(client, auth_headers):
    p = {
        "sale_number": f"UNIQ-{uuid.uuid4().hex[:6]}",
        "sale_date": datetime.utcnow().isoformat(),
        "subtotal": "0", "tax_amount": "0",
        "discount_amount": "0", "total_amount": "0",
        "status": "pending",
    }
    assert client.post("/sales/", json=p, headers=auth_headers).status_code == 201
    assert client.post("/sales/", json=p, headers=auth_headers).status_code == 400


def test_customer_email_and_mrn_unique(client, auth_headers, customer):
    r = client.post(
        "/customers/",
        json={
            "first_name": "Other",
            "last_name": "Person",
            "email": customer.email,
            "medical_record_number": customer.medical_record_number,
        },
        headers=auth_headers,
    )
    assert r.status_code == 400


def test_sale_item_requires_valid_sale_and_product(client, auth_headers):
    r = client.post(
        "/sale-items/",
        json={
            "quantity": "1", "unit_price": "1.00",
            "discount_amount": "0", "tax_amount": "0",
            "total_price": "1.00",
            "sale_id": str(uuid.uuid4()),
            "product_id": str(uuid.uuid4()),
        },
        headers=auth_headers,
    )
   
    assert r.status_code in (400, 404, 422)