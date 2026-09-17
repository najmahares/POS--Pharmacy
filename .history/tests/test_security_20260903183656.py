from app.core.security import hash_password, verify_password

def test_hash_and_verify_password():

    # Arrange

    password = "mysecretpassword"
    hashed_password = hash_password(password)
    assert isinstance(hashed_password, str)
    assert hashed_password != password  

    # Act


