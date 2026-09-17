def test_get_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_product(client, auth_headers):
    product_data = {
        "name": "Test Product",
        "sku": "TESTSKU123",
        "price": 9.99,
        "quantity": 100,
        "category_id": "00000000-0000-0000-0000-000000000000",
    }
    response = client.post("/products", json=product_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["name"] == product_data["name"]
    assert response.json()["sku"] == product_data["sku"]
    assert response.json()["price"] == product_data["price"]
    assert response.json()["name"] == product_data["name"]

def test_creating_product_without_name(client, auth_headers):
    product_data = {
        "sku": "TESTSKU123",
        "price": 9.99,
        "quantity": 100,
        "category_id": "00000000-0000-0000-0000-000000000000",
    }
    response = client.post("/products", json=product_data, headers=auth_headers)
    assert response.status_code == 422 