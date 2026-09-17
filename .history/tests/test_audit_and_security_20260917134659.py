import uuid
from datetime import datetime


def _sale_payload():
    return {
        "sale_number": f"SAL-{uuid.uuid4().hex[:8]}",
        "sale_date": datetime.utcnow().isoformat(),
        "subtotal": "10.00", "tax_amount": "0",
        "discount_amount": "0", "total_amount": "10.00",
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


import pytest


RBAC_MATRIX = [
   
    ("get",    "/users/",         "admin",              None, ["cashier", "pharmacist", "inventory-manager"]),
    ("get",    "/categories/",    "cashier",            None, []),  
    ("post",   "/categories/",    "inventory-manager",  {"name": "X"}, ["cashier", "pharmacist"]),
    ("delete", "/categories/{id}", "admin",             None, ["cashier", "pharmacist", "inventory-manager"]),
]


@pytest.mark.parametrize("method,path,allowed_role,payload,forbidden_roles", RBAC_MATRIX)
def test_rbac_matrix(client, method, path, allowed_role, payload, forbidden_roles,
                     admin_user, cashier_user, pharmacist_user, inventory_user, db_session):
    from app.core.security import create_access_token
    from app.models.category import Category

  
    cat = Category(id=uuid.uuid4(), name=f"RBAC-{uuid.uuid4().hex[:6]}", is_active=True)
    db_session.add(cat); db_session.commit()

    real_path = path.replace("{id}", str(cat.id))

    users = {
        "admin": admin_user, "cashier": cashier_user,
        "pharmacist": pharmacist_user, "inventory-manager": inventory_user,
    }

   
    tok = create_access_token(str(users[allowed_role].id))
    r = getattr(client, method)(real_path, headers={"Authorization": f"Bearer {tok}"},
                                **({"json": payload} if payload else {}))
    assert r.status_code not in (401, 403), f"{allowed_role} should access {method} {path}"

   
    for role in forbidden_roles:
        tok = create_access_token(str(users[role].id))
        r = getattr(client, method)(real_path, headers={"Authorization": f"Bearer {tok}"},
                                    **({"json": payload} if payload else {}))
        assert r.status_code == 403, f"{role} should NOT access {method} {path}"



def test_token_signed_with_wrong_key_rejected(client_no_auth):
    import jwt
    from datetime import datetime, timedelta, timezone
    forged = jwt.encode(
        {"sub": "any", "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
        "attacker-key",
        algorithm="HS256",
    )
    r = client_no_auth.get("/categories/", headers={"Authorization": f"Bearer {forged}"})
    assert r.status_code == 401


def test_token_for_nonexistent_user_rejected(client_no_auth):
    from app.core.security import create_access_token
    tok = create_access_token(str(uuid.uuid4()))       
    r = client_no_auth.get("/categories/", headers={"Authorization": f"Bearer {tok}"})
    assert r.status_code == 401


def test_inactive_user_token_rejected(client, inactive_headers):
    r = client.get("/categories/", headers=inactive_headers)
    assert r.status_code == 403


def test_expired_token_rejected(client_no_auth):
    from app.core.security import create_access_token
    from datetime import timedelta
    tok = create_access_token("any", expires_delta=timedelta(seconds=-1))
    r = client_no_auth.get("/categories/", headers={"Authorization": f"Bearer {tok}"})
    assert r.status_code == 401