import uuid
import jwt
from datetime import datetime, timedelta, timezone

import pytest


def test_hash_and_verify_password():
    from app.core.security import hash_password, verify_hash
    pw = "mysecretpassword"
    hashed = hash_password(pw)
    assert isinstance(hashed, str)
    assert hashed != pw
    assert hashed.startswith("$2")
    assert verify_hash(pw, hashed) is True
    assert verify_hash("wrong", hashed) is False


def test_hash_is_salted():
    from app.core.security import hash_password
    assert hash_password("same") != hash_password("same")


def test_create_access_token_returns_string():
    from app.core.security import create_access_token
    token = create_access_token("12345")
    assert isinstance(token, str)
    assert token.count(".") == 2


def test_decode_access_token_has_correct_claims():
    from app.core.security import create_access_token, decode_access_token
    token = create_access_token("12345")
    payload = decode_access_token(token)
    assert payload["sub"] == "12345"
    assert "exp" in payload
    assert "iat" in payload
    assert payload["exp"] > payload["iat"]


def test_create_and_decode_refresh_token():
    from app.core.security import create_refresh_token, decode_refresh_token
    token = create_refresh_token("12345")
    payload = decode_refresh_token(token)
    assert payload["sub"] == "12345"
    assert payload["type"] == "refresh"


def test_decode_refresh_token_rejects_access_token():
    from app.core.security import create_access_token, decode_refresh_token
    token = create_access_token("12345")
    with pytest.raises(ValueError):
        decode_refresh_token(token)


def test_expired_token_rejected(client_no_auth):
    from app.core.security import create_access_token
    token = create_access_token("test-user-id", expires_delta=timedelta(hours=-1))
    r = client_no_auth.get("/categories/", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401


def test_invalid_token_rejected(client_no_auth):
    r = client_no_auth.get(
        "/categories/",
        headers={"Authorization": "Bearer not-a-real-token"},
    )
    assert r.status_code == 401


def test_missing_token_rejected(client_no_auth):
    r = client_no_auth.get("/categories/")
    assert r.status_code == 401


def test_invalid_token_format_rejected(client_no_auth):
    r = client_no_auth.get(
        "/categories/",
        headers={"Authorization": "InvalidFormatToken"},
    )
    assert r.status_code == 401


def test_invalid_token_prefix_rejected(client_no_auth):
    r = client_no_auth.get(
        "/categories/",
        headers={"Authorization": "Token not-a-real-token"},
    )
    assert r.status_code == 401


def test_invalid_token_structure_rejected(client_no_auth):
    r = client_no_auth.get(
        "/categories/",
        headers={"Authorization": "Bearer"},
    )
    assert r.status_code == 401


def test_token_signed_with_wrong_key_rejected(client_no_auth):
    forged = jwt.encode(
        {"sub": "any", "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
        "attacker-key",
        algorithm="HS256",
    )
    r = client_no_auth.get(
        "/categories/",
        headers={"Authorization": f"Bearer {forged}"},
    )
    assert r.status_code == 401


def test_token_for_nonexistent_user_rejected(client_no_auth):
    from app.core.security import create_access_token
    token = create_access_token(str(uuid.uuid4()))
    r = client_no_auth.get(
        "/categories/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 401


def test_inactive_user_token_rejected(client, inactive_headers):
    r = client.get("/categories/", headers=inactive_headers)
    assert r.status_code == 403


def test_malformed_subject_rejected(client_no_auth):
    forged = jwt.encode(
        {"sub": "not-a-uuid", "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
        "attacker-key",
        algorithm="HS256",
    )
    r = client_no_auth.get(
        "/categories/",
        headers={"Authorization": f"Bearer {forged}"},
    )
    assert r.status_code == 401


def _sale_payload():
    return {
        "sale_number": f"SAL-{uuid.uuid4().hex[:8]}",
        "sale_date": datetime.utcnow().isoformat(),
        "subtotal": "10.00",
        "tax_amount": "0",
        "discount_amount": "0",
        "total_amount": "10.00",
        "status": "pending",
    }


def test_sale_user_id_comes_from_jwt_not_body(client, cashier_headers, cashier_user):
    payload = _sale_payload()
    payload["user_id"] = str(uuid.uuid4())
    r = client.post("/sales/", json=payload, headers=cashier_headers)
    assert r.status_code == 201
    assert r.json()["user_id"] == str(cashier_user.id)


def test_cashier_cannot_impersonate_admin(client, cashier_headers, admin_user):
    payload = _sale_payload()
    payload["user_id"] = str(admin_user.id)
    r = client.post("/sales/", json=payload, headers=cashier_headers)
    assert r.status_code == 201
    assert r.json()["user_id"] != str(admin_user.id)


def test_admin_cannot_forge_user_id_either(client, auth_headers, cashier_user):
    payload = _sale_payload()
    payload["user_id"] = str(cashier_user.id)
    r = client.post("/sales/", json=payload, headers=auth_headers)
    assert r.status_code == 201
    assert r.json()["user_id"] != str(cashier_user.id)


RBAC_MATRIX = [
    ("get", "/users/", "admin", None, ["cashier", "pharmacist", "inventory-manager"]),
    ("get", "/categories/", "cashier", None, []),
    ("get", "/products/", "cashier", None, []),
    ("get", "/customers/", "cashier", None, []),
    ("get", "/suppliers/", "cashier", None, []),
    ("get", "/sales/", "cashier", None, []),
    ("get", "/payments/", "cashier", None, []),
    ("get", "/receipts/", "cashier", None, []),
    ("get", "/sale-items/", "cashier", None, []),
]


@pytest.mark.parametrize("method,path,allowed_role,payload,forbidden_roles", RBAC_MATRIX)
def test_rbac_read_matrix(
    client,
    method,
    path,
    allowed_role,
    payload,
    forbidden_roles,
    admin_user,
    cashier_user,
    pharmacist_user,
    inventory_user,
):
    from app.core.security import create_access_token

    users = {
        "admin": admin_user,
        "cashier": cashier_user,
        "pharmacist": pharmacist_user,
        "inventory-manager": inventory_user,
    }

    token = create_access_token(str(users[allowed_role].id))
    r = getattr(client, method)(path, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code not in (401, 403)

    for role in forbidden_roles:
        token = create_access_token(str(users[role].id))
        r = getattr(client, method)(path, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 403


def test_create_category_inventory_ok_cashier_forbidden(
    client, inventory_headers, cashier_headers
):
    payload = {"name": f"RBAC-{uuid.uuid4().hex[:6]}"}
    assert client.post("/categories/", json=payload, headers=inventory_headers).status_code == 201
    assert client.post("/categories/", json=payload, headers=cashier_headers).status_code == 403


def test_create_product_inventory_ok_cashier_forbidden(
    client, inventory_headers, cashier_headers
):
    payload = {
        "name": "RBAC Product",
        "sku": f"RBAC-{uuid.uuid4().hex[:8]}",
        "unit_price": "1.00",
        "quantity_in_stock": 1,
        "reorder_level": 1,
        "expiry_date": "2030-01-01",
    }
    assert client.post("/products/", json=payload, headers=inventory_headers).status_code == 201
    payload["sku"] = f"RBAC-{uuid.uuid4().hex[:8]}"
    assert client.post("/products/", json=payload, headers=cashier_headers).status_code == 403


def test_delete_category_admin_ok_cashier_forbidden(
    client, auth_headers, cashier_headers
):
    created = client.post(
        "/categories/",
        json={"name": f"DEL-{uuid.uuid4().hex[:6]}"},
        headers=auth_headers,
    ).json()
    assert client.delete(f"/categories/{created['id']}", headers=cashier_headers).status_code == 403
    assert client.delete(f"/categories/{created['id']}", headers=auth_headers).status_code == 204


def test_delete_product_admin_ok_inventory_forbidden(
    client, auth_headers, inventory_headers
):
    payload = {
        "name": "DEL Product",
        "sku": f"DEL-{uuid.uuid4().hex[:8]}",
        "unit_price": "1.00",
        "quantity_in_stock": 1,
        "reorder_level": 1,
        "expiry_date": "2030-01-01",
    }
    created = client.post("/products/", json=payload, headers=inventory_headers).json()
    assert client.delete(f"/products/{created['id']}", headers=inventory_headers).status_code == 403
    assert client.delete(f"/products/{created['id']}", headers=auth_headers).status_code == 204


def test_delete_user_requires_admin(client, auth_headers, cashier_headers):
    payload = {
        "username": f"del_{uuid.uuid4().hex[:6]}",
        "email": f"del_{uuid.uuid4().hex[:6]}@test.com",
        "password": "Pass123!",
        "first_name": "D",
        "last_name": "U",
        "role": "cashier",
    }
    created = client.post("/users/", json=payload, headers=auth_headers).json()
    assert client.delete(f"/users/{created['id']}", headers=cashier_headers).status_code == 403
    assert client.delete(f"/users/{created['id']}", headers=auth_headers).status_code == 204


def test_cashier_cannot_list_users(client, cashier_headers):
    assert client.get("/users/", headers=cashier_headers).status_code == 403


def test_cashier_cannot_create_user(client, cashier_headers):
    payload = {
        "username": f"x_{uuid.uuid4().hex[:6]}",
        "email": f"x_{uuid.uuid4().hex[:6]}@test.com",
        "password": "Pass123!",
        "first_name": "X",
        "last_name": "Y",
        "role": "cashier",
    }
    assert client.post("/users/", json=payload, headers=cashier_headers).status_code == 403


def test_cashier_cannot_list_low_stock(client, cashier_headers):
    assert client.get("/products/low-stock", headers=cashier_headers).status_code == 403


def test_cashier_cannot_list_expired(client, cashier_headers):
    assert client.get("/products/expired", headers=cashier_headers).status_code == 403


def test_sale_status_update_requires_pharmacist(client, auth_headers, cashier_headers, pharmacist_headers):
    sale = client.post(
        "/sales/",
        json=_sale_payload(),
        headers=auth_headers,
    ).json()
    assert client.patch(
        f"/sales/{sale['id']}/status",
        params={"status": "completed"},
        headers=cashier_headers,
    ).status_code == 403
    assert client.patch(
        f"/sales/{sale['id']}/status",
        params={"status": "completed"},
        headers=pharmacist_headers,
    ).status_code == 200