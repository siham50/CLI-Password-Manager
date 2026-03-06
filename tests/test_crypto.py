from app import crypto

#pytest
def test_crypto():
    password = "1234"
    encrypted_password = crypto.encrypt_password(password).encode()
    assert crypto.decrypt_password(encrypted_password) == password