from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)
@pytest.fixture
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hospital Pharmacy POS System API", "status": "running"}


@pytest.fixture
def test_user(client, test_user):
    user_data = {
        "username": "testuser",
        "email": " hares@gmail.com",
        "password": "testpassword",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"] 

