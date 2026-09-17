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
