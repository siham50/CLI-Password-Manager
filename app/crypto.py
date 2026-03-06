from cryptography.fernet import Fernet, InvalidToken
import os


KEY_PATH = "data/key.key"

def ensure_data_folder():
    if not(os.path.exists("data/")):
        os.makedirs("data")


def generate_key():
    key = Fernet.generate_key()
    ensure_data_folder()
    with open (KEY_PATH, "wb") as file:
        file.write(key)
    return key


def load_key():
    try:
        with open (KEY_PATH, "rb") as file:
            data = file.read()
            if not data:
                return generate_key()
            else:
                return data
    except FileNotFoundError:
        return generate_key()


fernet_object = Fernet(load_key())

def encrypt_password(password : str) -> str:
        if not(isinstance(password, str)):
            raise TypeError
        elif password == "":
            raise ValueError
        return fernet_object.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password : bytes) -> str:
        if not(isinstance(encrypted_password, bytes)):
            raise TypeError
        elif encrypted_password == b"":
            raise ValueError
        try:
            return fernet_object.decrypt(encrypted_password).decode()
        except InvalidToken:
            raise