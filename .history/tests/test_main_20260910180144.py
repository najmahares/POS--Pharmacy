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


@pytest.fixture

def auth_headers(client, test_user):
    response = client.post(
        "auth/login",
        data={"username": "testuser", "password": "testpassword"}, #why not json here? because the login endpoint expects form data, not JSON
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

