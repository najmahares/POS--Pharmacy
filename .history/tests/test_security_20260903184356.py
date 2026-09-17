from app.core.security import hash_password, verify_hash
from app.core.security import create_access_token

def test_hash_and_verify_password():

    # Arrange

    password = "mysecretpassword"
    hashed_password = hash_password(password)
    assert isinstance(hashed_password, str)
    assert hashed_password != password  
    assert verify_hash(password, hashed_password) is True

def test_create_access_token():
    
    # Arrange
    user_id = "12345"
    token = create_access_token(user_id)
    assert isinstance(token, str)



