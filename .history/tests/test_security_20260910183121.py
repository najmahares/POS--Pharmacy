from datetime import timedelta

from app.core.security import (
    hash_password,
    verify_hash,
    create_access_token,
    decode_access_token,
)


def test_hash_and_verify_password():
    password = "mysecretpassword"
    hashed = hash_password(password)
    assert isinstance(hashed, str)
    assert hashed != password
    assert verify_hash(password, hashed) is True


def test_create_access_token():
    token = create_access_token("12345")
    assert isinstance(token, str)


def test_decode_access_token():
    token = create_access_token("12345")
    payload = decode_access_token(token)
    assert payload["sub"] == "12345"


def test_expired_token(client_no_auth):
    expired_token = create_access_token(
        "test-user-id",
        expires_delta=timedelta(hours=-1),
    )
    response = client_no_auth.get(
        "/products",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert response.status_code == 401


def test_invalid_token(client_no_auth):
    response = client_no_auth.get(
        "/products",
        headers={"Authorization": "Bearer not-a-real-token"},
    )
    assert response.status_code == 401

def test_missing_token(client_no_auth):
    response = client_no_auth.get("/products")
    assert response.status_code == 401  

def test_invalid_token_format(client_no_auth):
    response = client_no_auth.get(
        "/products",
        headers={"Authorization": "InvalidFormatToken"},
    )
    assert response.status_code == 401
def test_invalid_token_prefix(client_no_auth):
    response = client_no_auth.get(
        "/products",
        headers={"Authorization": "Token not-a-real-token"},
    )
    assert response.status_code == 401

def test_invalid_token_structure(client_no_auth):
    response = client_no_auth.get(
        "/products",
        headers={"Authorization": "Bearer"},
    )   
    