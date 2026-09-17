import uuid


def test_get_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_product(client, auth_headers):
    product_data = {
        "name": "Test Product",
        "sku": f"TESTSKU-{uuid.uuid4().hex[:8]}",
        "price": "9.99",
        "cost": "5.00",
        "quantity_in_stock": 100,
        "reorder_level": 10,
        "category_id": None,
        "supplier_id": None,
    }
    response = client.post("/products", json=product_data, headers=auth_headers)
    assert response.status_code == 201, response.json()
    assert response.json()["name"] == product_data["name"]


def test_creating_product_without_name(client, auth_headers):
    product_data = {
        "sku": f"NO-NAME-{uuid.uuid4().hex[:8]}",
        "price": "9.99",
        "cost": "5.00",
        "quantity_in_stock": 100,
        "reorder_level": 10,
    }
    response = client.post("/products", json=product_data, headers=auth_headers)
    assert response.status_code == 422

def test_update_product(client, auth_headers):

    product_data = {
        "name": "Product to Update",
        "sku": f"UPDATE-{uuid.uuid4().hex[:8]}",
        "price": "19.99",
        "cost": "10.00",
        "quantity_in_stock": 50,
        "reorder_level": 5,
    }
    create_response = client.post("/products", json=product_data, headers=auth_headers)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    
    updated_data = {
        "name": "Updated Product Name",
        "price": "29.99",
    }
    update_response = client.put(f"/products/{product_id}", json=updated_data, headers=auth_headers)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == updated_data["name"]
    assert update_response.json()["price"] == updated_data["price"] 